import abc
import re
from collections.abc import Iterable
from typing import Any, Never, assert_never

from yabra.doc import types
from yabra.doc.exc import InvalidDocumentError


class DocumentSpecification(abc.ABC):
    MAX_LENGTH: int
    NUM_OF_CHECK_DIGITS: int
    VALID_DIGITS_RE: re.Pattern[str]
    REPEATED_DIGITS_ALLOWED: bool = False
    DEFAULT_FILTERED_VALUE_MASK: str

    @staticmethod
    @abc.abstractmethod
    def digit_value_for_check_digit(digit: str) -> int: ...

    @staticmethod
    @abc.abstractmethod
    def digit_weights_iterable(n_of_current_digits: int) -> Iterable[int]: ...

    @classmethod
    @abc.abstractmethod
    def calculate_next_check_digit(cls, digits: str) -> str: ...

    @classmethod
    def calculate_document_number(cls, digits: str) -> str:
        digits_to_check = digits[: cls.MAX_LENGTH - cls.NUM_OF_CHECK_DIGITS]
        for _ in range(cls.NUM_OF_CHECK_DIGITS):
            digits_to_check += cls.calculate_next_check_digit(digits_to_check)

        assert len(digits_to_check) == cls.MAX_LENGTH
        return digits_to_check

    @staticmethod
    def parse_raw_value(value: Any) -> str | None: ...


class BaseDoc(abc.ABC):
    spec: type[DocumentSpecification]

    def __init__(self, value: Any) -> None:
        self.raw_value = value
        self._validated_value: str | None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.raw_value!r})"

    def __str__(self) -> str:
        if self._validated_value is not None:
            return self._validated_value
        return self.validated_value()

    def validated_value(self) -> str:
        if self._validated_value is not None:
            return self._validated_value

        result = self.perform_validation()
        if result["ok"] is True:
            self._validated_value = result["value"]
            return self._validated_value
        self.raise_invalid_document_error(result)
        assert_never("`raise_invalid_document_error` didn't raised an exception")

    def perform_validation(self) -> types.PerformValidationResult:
        value = self.spec.parse_raw_value(self.raw_value)
        if value is None:
            return {
                "ok": False,
                "violation": "INVALID_TYPE",
                "message": f"Documento inválido: Tipo {type(self.raw_value).__name__!r} não suportado",
                "extra": {"type": type(self.raw_value).__name__, "raw": repr(self.raw_value)},
            }
        digits = self.spec.VALID_DIGITS_RE.sub(repl="", string=value)
        if not digits:
            return {
                "ok": False,
                "violation": "INVALID_VALUE",
                "message": "Documento inválido: Nenhum dígito encontrado",
                "extra": {"value": value, "raw": repr(self.raw_value)},
            }
        if len(digits) != self.spec.MAX_LENGTH:
            return {
                "ok": False,
                "violation": "INVALID_LENGTH",
                "message": f"Documento inválido: Número de dígitos inválido, esperavam-se {self.spec.MAX_LENGTH} dígitos",
                "extra": {"expected_length": self.spec.MAX_LENGTH, "length": len(digits)},
            }

        if not self.spec.REPEATED_DIGITS_ALLOWED and len(set(digits)) == 1:
            return {
                "ok": False,
                "violation": "INVALID_VALUE",
                "message": "Documento inválido: Documento com números repetidos não é permitido",
                "extra": {"value": digits},
            }

        calculated_doc = self.spec.calculate_document_number(digits)
        if calculated_doc != digits:
            return {
                "ok": False,
                "violation": "INVALID_CHECK_DIGIT",
                "message": "Documento inválido: Os dígitos verificadores não coincidem",
                "extra": {"calculated": calculated_doc, "received": digits},
            }
        return {"ok": True, "value": digits.upper()}

    def raise_invalid_document_error(self, result: types.PerformValidationErrorResult) -> Never:
        raise InvalidDocumentError(result)

    @abc.abstractmethod
    def masked_value(self) -> str: ...

    @abc.abstractmethod
    def filtered_value(self, mask: str | None = None) -> str: ...


class Mod11CheckDigitsSpecification(DocumentSpecification):
    @classmethod
    def calculate_next_check_digit(cls, digits: str) -> str:
        weights = cls.digit_weights_iterable(len(digits))
        digits_sum = sum(
            cls.digit_value_for_check_digit(digit) * weight
            for digit, weight in zip(digits, weights, strict=True)
        )
        remainder = digits_sum % 11
        return "0" if remainder <= 1 else str(11 - remainder)

    @staticmethod
    def parse_raw_value(value: Any) -> str | None:
        if isinstance(value, str):
            return value
        if isinstance(value, bytes):
            return value.decode()
        if isinstance(value, int):
            return str(value)
        return None
