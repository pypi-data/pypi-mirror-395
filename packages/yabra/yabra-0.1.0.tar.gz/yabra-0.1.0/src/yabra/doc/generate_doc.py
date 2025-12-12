import itertools
import random
import string
from typing import Generator, Literal, Protocol, assert_never

from yabra.doc.base_doc import BaseDoc
from yabra.doc.cnpj import CNPJ
from yabra.doc.cpf import CPF


class MissingDigitsGenerator(Protocol):
    population: str

    def __init__(self) -> None: ...
    def get_digits(self, n: int) -> str: ...


class RandomAlphaNumericDigitsGenerator(MissingDigitsGenerator):
    def __init__(self) -> None:
        self.population = string.ascii_uppercase + string.digits

    def get_digits(self, n: int) -> str:
        return "".join(random.choices(self.population, k=n))


class RandomMissingDigitsGenerator(MissingDigitsGenerator):
    def __init__(self) -> None:
        self.population = string.digits

    def get_digits(self, n: int) -> str:
        return "".join(random.choices(self.population, k=n))


class SequentialMissingDigitsGenerator(MissingDigitsGenerator):
    def __init__(self) -> None:
        self.population = string.digits
        self.seq_range_iter = iter(range(999_999_999_999))

    def get_digits(self, n: int) -> str:
        digits = str(next(self.seq_range_iter))
        return digits.zfill(n)


class SequentialAlphaNumericMissingDigitsGenerator(MissingDigitsGenerator):
    def __init__(self) -> None:
        self.population = string.digits + string.ascii_uppercase
        self._iter = self._next_digit_iter()

    def get_digits(self, n: int) -> str:
        digits = next(self._iter)
        return digits.zfill(n)

    def _next_digit_iter(self) -> Generator[str, None, None]:
        length = 1
        while True:
            for combo in itertools.product(self.population, repeat=length):
                yield "".join(combo)
            length += 1


SupportedDocTypes = Literal["cpf", "cnpj"]


def get_doc_type_class(doc_type: SupportedDocTypes) -> type[BaseDoc]:
    if doc_type == "cpf":
        return CPF
    if doc_type == "cnpj":
        return CNPJ
    assert_never(doc_type)


SupportedMissingDigitsAlgorithm = Literal[
    "random", "alpha_random", "sequential", "alpha_sequential"
]


def get_missing_digits_algorithm_generator(
    algorithm: SupportedMissingDigitsAlgorithm,
) -> MissingDigitsGenerator:
    if algorithm == "random":
        return RandomMissingDigitsGenerator()
    if algorithm == "alpha_random":
        return RandomAlphaNumericDigitsGenerator()
    if algorithm == "sequential":
        return SequentialMissingDigitsGenerator()
    if algorithm == "alpha_sequential":
        return SequentialAlphaNumericMissingDigitsGenerator()
    assert_never(algorithm)


class DocumentGenerator:
    def __init__(
        self,
        doc_type: SupportedDocTypes,
        algorithm: SupportedMissingDigitsAlgorithm,
        prefix: str,
        number: int,
    ) -> None:
        self.doc_class = get_doc_type_class(doc_type)
        self.spec = self.doc_class.spec
        self.prefix_digits_max_length = self.spec.MAX_LENGTH - self.spec.NUM_OF_CHECK_DIGITS
        self.missing_digits_generator = self._get_valid_missing_digits_generator(algorithm)
        self.prefix = self._get_valid_prefix(prefix)
        self.number = self._get_valid_number(number)

    def _get_valid_missing_digits_generator(
        self, algorithm: SupportedMissingDigitsAlgorithm
    ) -> MissingDigitsGenerator:
        if algorithm == "random" or algorithm == "sequential":
            return get_missing_digits_algorithm_generator(algorithm)
        if algorithm == "alpha_random" or algorithm == "alpha_sequential":
            # Alpha numeric validation
            doc_allows_alpha_chars = self.spec.VALID_DIGITS_RE.sub("", "A")
            if not doc_allows_alpha_chars:
                raise ValueError("Incompatible algorithm for doc_type")

            return get_missing_digits_algorithm_generator(algorithm)
        assert_never(algorithm)

    def _get_valid_prefix(self, prefix: str) -> str:
        valid_prefix_digits = "".join(
            d for d in prefix if d in self.missing_digits_generator.population
        )
        if valid_prefix_digits != prefix:
            raise ValueError(
                f"Invalid prefix option, it contains invalid digits. Valid digits: {self.missing_digits_generator.population!r}",
                "You might want to verify if the provided prefix is compatible with the selected algorithm",
            )
        if len(valid_prefix_digits) > self.prefix_digits_max_length:
            raise ValueError(
                f"Invalid prefix option, it must not have length > {self.prefix_digits_max_length}"
            )
        return prefix

    def _get_valid_number(self, number: int) -> int:
        if number < 0:
            raise ValueError("Invalid number option, it must value must be greater than 0")

        doc_possibilities = len(self.missing_digits_generator.population) ** (
            self.prefix_digits_max_length - len(self.prefix)
        )
        if number > doc_possibilities:
            raise ValueError(
                f"Invalid number option, the required value is above the maximum number of possibilities ({doc_possibilities})"
            )
        return number

    def iter_documents(self) -> Generator[BaseDoc, None, None]:
        generated_docs = set[str]()
        iter_count = 0
        max_iter_count = self.number * 5
        # Useful for the random missing digits generator, since its not deterministic, we must define a maximum
        # number of iterations in order to not end up in a infinite loop

        while len(generated_docs) < self.number and iter_count < max_iter_count:
            iter_count += 1
            document = self._generate_one()
            if document.validated_value() in generated_docs:
                continue
            generated_docs.add(document.validated_value())
            yield document

    def _generate_one(self) -> BaseDoc:
        digits = self.prefix

        missing_digits = self.prefix_digits_max_length - len(digits)
        assert missing_digits >= 0

        if missing_digits:
            digits += self.missing_digits_generator.get_digits(n=missing_digits)
        return self.doc_class(self.spec.calculate_document_number(digits))
