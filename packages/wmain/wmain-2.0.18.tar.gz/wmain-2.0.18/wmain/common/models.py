from functools import lru_cache
from typing import Any, Dict, List, Callable, Union, Set, ClassVar, Mapping as TypingMapping
from collections import defaultdict
from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_snake


# --- Utility: Cached Conversion ---
@lru_cache
def cached_to_snake(text: str) -> str:
    """Caches the result of Pydantic's to_snake conversion."""
    return to_snake(text)


# --- Exception Definitions ---

class ModelException(Exception):
    """Base exception for all model-related errors."""
    pass


class UnexpectedModelInputError(ModelException):
    """Raised when the input is not a mapping or when an unsupported key type is encountered."""
    pass


class KeyConflictError(ModelException):
    """Raised when multiple input keys would map to the same canonical snake_case field."""
    pass


# --- Recursive Normalization Logic ---

TransformedData = Union[Dict[str, Any], List[Any], Any]


def _recursive_normalise(data: Any, to_snake_func: Callable[[str], str]) -> TransformedData:
    """Recursively converts all keys in Mappings/Dicts to snake_case and detects conflicts."""
    if isinstance(data, Mapping):
        normalised_data: Dict[str, Any] = {}
        key_origins: Dict[str, list[Any]] = defaultdict(list)

        for raw_key, value in data.items():
            if not isinstance(raw_key, (str, int)):
                raise UnexpectedModelInputError(
                    f"Only string and integer keys supported, got {type(raw_key)!r}"
                )

            raw_key_str = str(raw_key)
            snake_key = to_snake_func(raw_key_str)

            key_origins[snake_key].append(raw_key)
            normalised_data[snake_key] = _recursive_normalise(value, to_snake_func)

        conflicts = {k: v for k, v in key_origins.items() if len(v) > 1}
        if conflicts:
            lines = [
                f"Conflict: {', '.join(repr(k) for k in conflict_keys)} => {snake_key}"
                for snake_key, conflict_keys in conflicts.items()
            ]
            raise KeyConflictError(
                "Multiple input keys map to the same field at a nested level:\n"
                + "\n".join(lines)
            )

        return normalised_data

    elif isinstance(data, list):
        return [_recursive_normalise(item, to_snake_func) for item in data]

    return data


# --- Core Matching Helper Functions (Refactored) ---

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


def _normalize_value_if_needed(
        value: Any, target_field_name: str, no_recursion_fields: Set[str]
) -> Any:
    """
    Applies recursive normalization to the value unless the field is configured to skip it.
    """
    if target_field_name in no_recursion_fields:
        # Skip recursion (e.g., for JSON fields or fields that handle keys internally)
        return value
    else:
        # Recursively normalize nested keys
        return _recursive_normalise(value, cached_to_snake)


def _match_keys_to_fields(
        data: TypingMapping[Any, Any],
        snake_to_original_field_map: Dict[str, str],
        no_recursion_fields: Set[str]
) -> Dict[str, Any]:
    """
    Performs top-level matching, key conversion, and selective value normalization.
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

            processed_data[target_field_name] = _normalize_value_if_needed(
                value, target_field_name, no_recursion_fields
            )
        # Unmatched keys are ignored per model_config

    _check_top_level_conflict(key_origins)

    return processed_data


# --- Core Pydantic Base Class ---

class AutoMatchModel(BaseModel):
    """
    Pydantic base model for flexible key matching (camelCase/snake_case)
    and selective recursive normalization.
    """

    # Set of original field names to skip recursive key normalization
    _NO_RECURSIVE_FIELDS: ClassVar[Set[str]] = set()

    model_config = ConfigDict(
        populate_by_name=True,  # Allows populating using original field names
        extra="ignore",  # Ignores unmatched fields in the input
    )

    @model_validator(mode="before")
    def _match_and_process_keys(cls, data: Any) -> TransformedData:
        """Pydantic pre-validation step to match input keys to model fields."""
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

        # 2. Get the set of fields that skip recursion
        no_recursion_fields = cls._NO_RECURSIVE_FIELDS

        # 3. Execute matching and processing
        return _match_keys_to_fields(data, snake_to_original_field_map, no_recursion_fields)
