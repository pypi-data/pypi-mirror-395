import re
from collections.abc import Iterable

from yabra.doc.base_doc import BaseDoc, Mod11CheckDigitsSpecification


class CPFSpecification(Mod11CheckDigitsSpecification):
    MAX_LENGTH = 11
    NUM_OF_CHECK_DIGITS = 2
    VALID_DIGITS_RE = re.compile(r"\D")
    DEFAULT_FILTERED_VALUE_MASK = "{0}.***.***-{3}"

    @staticmethod
    def digit_value_for_check_digit(digit: str) -> int:
        return int(digit)

    @staticmethod
    def digit_weights_iterable(n_of_current_digits: int) -> Iterable[int]:
        return range(n_of_current_digits + 1, 1, -1)


class CPF(BaseDoc):
    spec = CPFSpecification

    def masked_value(self) -> str:
        cpf = self.validated_value()
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

    def filtered_value(self, mask: str | None = None) -> str:
        mask = mask or self.spec.DEFAULT_FILTERED_VALUE_MASK
        cpf = self.validated_value()
        return mask.format(*[cpf[:3], cpf[3:6], cpf[6:9], cpf[9:11]])
