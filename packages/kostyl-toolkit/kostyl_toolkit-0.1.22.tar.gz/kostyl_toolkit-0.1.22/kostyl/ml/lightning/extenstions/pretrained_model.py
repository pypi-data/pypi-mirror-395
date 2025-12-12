from pathlib import Path
from typing import Any
from typing import cast

import torch
from transformers import PretrainedConfig
from transformers import PreTrainedModel


try:
    from peft import PeftConfig
except ImportError:
    PeftConfig = None  # ty: ignore

from kostyl.utils.logging import log_incompatible_keys
from kostyl.utils.logging import setup_logger
from torch import nn


logger = setup_logger("LightningPretrainedModelMixin", fmt="only_message")


class LightningCheckpointLoaderMixin(PreTrainedModel):
    """A mixin class for loading pretrained models from PyTorch Lightning checkpoints."""

    @classmethod
    def from_lighting_checkpoint[TModelInstance: LightningCheckpointLoaderMixin](  # noqa: C901
        cls: type[TModelInstance],
        checkpoint_path: str | Path,
        config_key: str = "config",
        weights_prefix: str = "model.",
        should_log_incompatible_keys: bool = True,
        **kwargs: Any,
    ) -> TModelInstance:
        """
        Load a model from a Lightning checkpoint file.

        This class method loads a pretrained model from a PyTorch Lightning checkpoint file (.ckpt).
        It extracts the model configuration from the checkpoint, instantiates the model, and loads
        the state dictionary, handling any incompatible keys.

        Note:
            The method uses `torch.load` with `weights_only=False` and `mmap=True` for loading.
            Incompatible keys (missing, unexpected, mismatched) are collected and optionally logged.

        Args:
            cls (type["LightningPretrainedModelMixin"]): The class of the model to instantiate.
            checkpoint_path (str | Path): Path to the checkpoint file. Must be a .ckpt file.
            config_key (str, optional): Key in the checkpoint dictionary where the config is stored.
                Defaults to "config".
            weights_prefix (str, optional): Prefix to strip from state dict keys. Defaults to "model.".
                If not empty and doesn't end with ".", a "." is appended.
            should_log_incompatible_keys (bool, optional): Whether to log incompatible keys. Defaults to True.
            **kwargs: Additional keyword arguments to pass to the model loading method.

        Returns:
            TModelInstance: The loaded model instance.

        Raises:
            ValueError: If checkpoint_path is a directory, not a .ckpt file, or invalid.
            FileNotFoundError: If the checkpoint file does not exist.

        """
        if isinstance(checkpoint_path, str):
            checkpoint_path = Path(checkpoint_path)

        if checkpoint_path.is_dir():
            raise ValueError(f"{checkpoint_path} is a directory")
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"{checkpoint_path} does not exist")
        if checkpoint_path.suffix != ".ckpt":
            raise ValueError(f"{checkpoint_path} is not a .ckpt file")

        checkpoint_dict = torch.load(
            checkpoint_path,
            map_location="cpu",
            weights_only=False,
            mmap=True,
        )

        # 1. Восстанавливаем конфиг
        config_cls = cast(type[PretrainedConfig], cls.config_class)
        config_dict = checkpoint_dict[config_key]
        config_dict.update(kwargs)
        config = config_cls.from_dict(config_dict)

        kwargs_for_model: dict[str, Any] = {}
        for key, value in kwargs.items():
            if not hasattr(config, key):
                kwargs_for_model[key] = value

        with torch.device("meta"):
            model = cls(config, **kwargs_for_model)

            # PEFT-адаптеры (оставляю твою логику как есть)
            if "peft_config" in checkpoint_dict:
                if PeftConfig is None:
                    raise ImportError(
                        "peft is not installed. Please install it to load PEFT models."
                    )
                for name, adapter_dict in checkpoint_dict["peft_config"].items():
                    peft_cfg = PeftConfig.from_peft_type(**adapter_dict)
                    model.add_adapter(peft_cfg, adapter_name=name)

        incompatible_keys: dict[str, list[str]] = {}

        raw_state_dict: dict[str, torch.Tensor] = checkpoint_dict["state_dict"]

        if weights_prefix:
            if not weights_prefix.endswith("."):
                weights_prefix = weights_prefix + "."
            state_dict: dict[str, torch.Tensor] = {}
            mismatched_keys: list[str] = []

            for key, value in raw_state_dict.items():
                if key.startswith(weights_prefix):
                    new_key = key[len(weights_prefix) :]
                    state_dict[new_key] = value
                else:
                    mismatched_keys.append(key)

            if mismatched_keys:
                incompatible_keys["mismatched_keys"] = mismatched_keys
        else:
            state_dict = raw_state_dict

        # 5. Логика base_model_prefix как в HF:
        #    поддержка загрузки базовой модели <-> модели с головой
        #
        # cls.base_model_prefix обычно "model" / "bert" / "encoder" и т.п.
        base_prefix: str = getattr(cls, "base_model_prefix", "") or ""
        model_to_load: nn.Module = model

        if base_prefix:
            prefix_with_dot = base_prefix + "."
            loaded_keys = list(state_dict.keys())
            full_model_state = model.state_dict()
            expected_keys = list(full_model_state.keys())

            has_prefix_module = any(k.startswith(prefix_with_dot) for k in loaded_keys)
            expects_prefix_module = any(
                k.startswith(prefix_with_dot) for k in expected_keys
            )

            # Кейc 1: загружаем базовую модель в модель с головой.
            # Пример: StaticEmbeddingsForSequenceClassification (имеет .model)
            #         state_dict с ключами "embeddings.weight", "token_pos_weights", ...
            if (
                hasattr(model, base_prefix)
                and not has_prefix_module
                and expects_prefix_module
            ):
                # Веса без префикса -> грузим только в model.<base_prefix>
                model_to_load = getattr(model, base_prefix)

            # Кейc 2: загружаем чекпоинт модели с головой в базовую модель.
            # Пример: BertModel, а в state_dict ключи "bert.encoder.layer.0..."
            elif (
                not hasattr(model, base_prefix)
                and has_prefix_module
                and not expects_prefix_module
            ):
                new_state_dict: dict[str, torch.Tensor] = {}
                for key, value in state_dict.items():
                    if key.startswith(prefix_with_dot):
                        new_key = key[len(prefix_with_dot) :]
                    else:
                        new_key = key
                    new_state_dict[new_key] = value
                state_dict = new_state_dict

        load_result = model_to_load.load_state_dict(
            state_dict, strict=False, assign=True
        )
        missing_keys, unexpected_keys = (
            load_result.missing_keys,
            load_result.unexpected_keys,
        )

        # Если мы грузили только в base-подмодуль, расширим missing_keys
        # до полного списка (base + голова), как в старых версиях HF.
        if model_to_load is not model and base_prefix:
            base_keys = set(model_to_load.state_dict().keys())
            # Приводим ключи полной модели к "безпрефиксному" виду
            head_like_keys = set()
            prefix_with_dot = base_prefix + "."
            for k in model.state_dict().keys():
                if k.startswith(prefix_with_dot):
                    # отрезаем "model."
                    head_like_keys.add(k[len(prefix_with_dot) :])
                else:
                    head_like_keys.add(k)
            extra_missing = sorted(head_like_keys - base_keys)
            missing_keys = list(missing_keys) + extra_missing

        incompatible_keys["missing_keys"] = missing_keys
        incompatible_keys["unexpected_keys"] = unexpected_keys

        if should_log_incompatible_keys:
            log_incompatible_keys(incompatible_keys=incompatible_keys, logger=logger)

        return model
