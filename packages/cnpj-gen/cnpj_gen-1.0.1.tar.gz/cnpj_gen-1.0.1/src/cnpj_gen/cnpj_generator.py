import random

from cnpj_cd import CnpjCheckDigits

from .cnpj_generator_options import CnpjGeneratorOptions


class CnpjGenerator:
    """Class to generate a valid CNPJ according to the given options."""

    __slots__ = "_options"

    def __init__(self, format: bool | None = None, prefix: str | None = None):
        self._options = CnpjGeneratorOptions(format, prefix)

    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        """Executes the CNPJ generation, overriding any given options with the ones set on the generator instance."""
        actual_options = self._options.merge(format, prefix)

        prefix_numbers = [int(digit) for digit in actual_options.prefix]

        business_id = self._generate_business_id(prefix_numbers)
        branch_id = self._generate_branch_id(prefix_numbers)
        cnpj_sequence = business_id + branch_id

        cnpj_check_digits = CnpjCheckDigits(cnpj_sequence)
        cnpj_generated = cnpj_check_digits.to_string()

        if actual_options.format:
            return self._format(cnpj_generated)

        return cnpj_generated

    def _generate_business_id(self, prefix_numbers: list[int]) -> list[int]:
        business_id_length = 8

        business_id_start = prefix_numbers[:business_id_length]
        business_id_start_length = len(business_id_start)

        business_id_end = [
            random.randint(0, 9)
            for _ in range(business_id_length - business_id_start_length)
        ]

        return business_id_start + business_id_end

    def _generate_branch_id(self, prefix_numbers: list[int]) -> list[int]:
        branch_id_length = 4

        branch_id_start = prefix_numbers[8 : 8 + branch_id_length]
        branch_id_start_length = len(branch_id_start)

        branch_id_end = [0] * (branch_id_length - branch_id_start_length)
        branch_id_end_length = len(branch_id_end)

        if branch_id_end_length > 0:
            branch_id_end[branch_id_end_length - 1] = random.randint(1, 9)

        return branch_id_start + branch_id_end

    def _format(self, cnpj_string: str) -> str:
        return (
            f"{cnpj_string[0:2]}.{cnpj_string[2:5]}.{cnpj_string[5:8]}/"
            f"{cnpj_string[8:12]}-{cnpj_string[12:14]}"
        )

    @property
    def options(self) -> CnpjGeneratorOptions:
        """Direct access to the options manager for the CNPJ generator."""
        return self._options
