import itertools
import re
from collections.abc import Iterable

from yabra.doc.base_doc import BaseDoc, Mod11CheckDigitsSpecification


class AlphaNumericCNPJSpecification(Mod11CheckDigitsSpecification):
    """Alpha-numeric CNPJ specification, validates both numeric and alpha-numeric documents"""

    MAX_LENGTH = 14
    NUM_OF_CHECK_DIGITS = 2
    VALID_DIGITS_RE = re.compile(r"[^A-Za-z0-9]")
    DEFAULT_FILTERED_VALUE_MASK = "{0}.***.{2}/****-{4}"

    @staticmethod
    def digit_value_for_check_digit(digit: str) -> int:
        # Ascii value of the digit - constant value 48
        return ord(digit.upper()) - 48

    @staticmethod
    def digit_weights_iterable(n_of_current_digits: int) -> Iterable[int]:
        # The weights starts from 2 and increase up to 9 (range), and start over (cycle).
        # The weight starts from right to left (reversed)
        return reversed(list(itertools.islice(itertools.cycle(range(2, 10)), n_of_current_digits)))


class NumericCNPJSpecification(AlphaNumericCNPJSpecification):
    """Accepts only the numeric form of the CNPJ document, the key difference is how the value is calculated
    for the check digits, before it's way simpler"""

    VALID_DIGITS_RE = re.compile(r"\D")

    @staticmethod
    def digit_value_for_check_digit(digit: str) -> int:
        return int(digit)


class CNPJ(BaseDoc):
    spec = AlphaNumericCNPJSpecification

    def masked_value(self) -> str:
        cnpj = self.validated_value()
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

    def filtered_value(self, mask: str | None = None) -> str:
        mask = mask or self.spec.DEFAULT_FILTERED_VALUE_MASK
        cnpj = self.validated_value()
        return mask.format(*[cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14]])
