from typing import Any, Literal, TypedDict

DocumentValidationViolation = Literal[
    "INVALID_TYPE", "INVALID_LENGTH", "INVALID_VALUE", "INVALID_CHECK_DIGIT"
]


class _PerformValidationOkResult(TypedDict):
    ok: Literal[True]
    value: str


class PerformValidationErrorResult(TypedDict):
    ok: Literal[False]
    violation: DocumentValidationViolation
    message: str
    extra: dict[str, Any]


PerformValidationResult = PerformValidationErrorResult | _PerformValidationOkResult
