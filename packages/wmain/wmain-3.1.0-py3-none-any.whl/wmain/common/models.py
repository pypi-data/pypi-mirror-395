from functools import lru_cache
from typing import Any, Dict, Mapping as TypingMapping
from collections import defaultdict
from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_snake


# --- Utility: Cached Conversion ---
@lru_cache
def cached_to_snake(text: str) -> str:
    """Caches the result of Pydantic's to_snake conversion."""
    return to_snake(text)


# --- Exception Definitions (Unchanged) ---
class ModelException(Exception): pass
class UnexpectedModelInputError(ModelException): pass
class KeyConflictError(ModelException): pass


# --- Core Matching Helper Functions (Modified to be TOP-LEVEL ONLY) ---

def _check_top_level_conflict(key_origins: Dict[str, list[Any]]):
    """Checks for conflicts where multiple input keys map to the same canonical snake_key."""
    conflicts = {k: v for k, v in key_origins.items() if len(v) > 1}
    if conflicts:
        lines = [
            f"Conflict: {', '.join(repr(k) for k in conflict_keys)} => {input_snake_key}"
            for input_snake_key, conflict_keys in conflicts.items()
        ]
        raise KeyConflictError(
            "Multiple input keys map to the same field at the top level:\n"
            + "\n".join(lines)
        )


def _match_keys_to_fields(
        data: TypingMapping[Any, Any],
        snake_to_original_field_map: Dict[str, str],
) -> Dict[str, Any]:
    """
    Performs TOP-LEVEL matching and key conversion. Values are passed through unchanged.
    Keys in the output dictionary are the model's **original field names**.
    """
    processed_data: Dict[str, Any] = {}
    key_origins: Dict[str, list[Any]] = defaultdict(list)

    for raw_key, value in data.items():
        if not isinstance(raw_key, (str, int)):
            raise UnexpectedModelInputError(
                f"Only string and integer keys supported, got {type(raw_key)!r}"
            )

        raw_key_str = str(raw_key)
        input_snake_key = cached_to_snake(raw_key_str)

        # Record raw key for conflict check
        key_origins[input_snake_key].append(raw_key)

        # Match against canonical fields
        if input_snake_key in snake_to_original_field_map:
            target_field_name = snake_to_original_field_map[input_snake_key]

            # ⚠️ 关键修改: 直接赋值，不再对 value 进行任何递归处理。
            # Pydantic 将自行处理嵌套的 BaseModel 或类型转换。
            processed_data[target_field_name] = value
        # Unmatched keys are ignored per model_config

    _check_top_level_conflict(key_origins)

    return processed_data


# --- Core Pydantic Base Class (Modified) ---

class AutoMatchModel(BaseModel):
    """
    Pydantic base model for flexible key matching (camelCase/snake_case)
    at the TOP LEVEL ONLY. Nested dictionaries keys are preserved.
    """

    # 递归控制逻辑被移除
    # _NO_RECURSIVE_FIELDS: ClassVar[Set[str]] = set()

    model_config = ConfigDict(
        populate_by_name=True,  # Allows populating using original field names
        extra="ignore",  # Ignores unmatched fields in the input
    )

    @model_validator(mode="before")
    def _match_and_process_keys(cls, data: Any) -> Any: # Type hint simplified
        """Pydantic pre-validation step to match input keys to model fields (Top-level only)."""
        if not isinstance(data, Mapping):
            raise UnexpectedModelInputError(
                f"Expected a mapping (e.g., dict), got {type(data).__name__}"
            )

        # 1. Map canonical snake_key to the model's original field name
        snake_to_original_field_map: Dict[str, str] = {}
        for original_field_name in cls.model_fields.keys():
            snake_key = cached_to_snake(original_field_name)

            if snake_key in snake_to_original_field_map:
                # Check for field definition conflict
                raise KeyConflictError(
                    f"Model field definition conflict: '{original_field_name}' maps to "
                    f"the same canonical key '{snake_key}' as "
                    f"'{snake_to_original_field_map[snake_key]}' in the model."
                )

            snake_to_original_field_map[snake_key] = original_field_name

        # 2. Execute TOP-LEVEL matching
        # ⚠️ 注意: 移除了 no_recursion_fields 参数
        return _match_keys_to_fields(data, snake_to_original_field_map)
