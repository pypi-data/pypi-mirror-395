from typing import Any, Callable, Dict, Mapping

from jsonschema.validators import Draft4Validator  # type: ignore[import-untyped]

PartialDraft4Validator: type[Draft4Validator]

def _generate_legacy_type_checks(
    types: Mapping[str, type | tuple[type, ...]],
) -> Dict[str, Callable[[Any, Any], bool]]: ...
def _create_validator(
    schema: Any,
    base_validator_cls: type | None = ...,
    custom_checks: Mapping[str, type | tuple[type, ...]] | None = ...,
) -> type: ...
