import re
from dataclasses import dataclass, replace

from .exceptions import (
    CnpjGeneratorInvalidPrefixBranchIdError,
    CnpjGeneratorInvalidPrefixLengthError,
)

CNPJ_LENGTH = 14


@dataclass(slots=True, frozen=False)
class CnpjGeneratorOptions:
    """Class to manage and store the options for the CNPJ generator."""

    format: bool | None = None
    prefix: str | None = None

    def __post_init__(self) -> None:
        if self.format is None:
            object.__setattr__(self, "format", False)
        if self.prefix is None:
            object.__setattr__(self, "prefix", "")

    def merge(
        self,
        format: bool | None = None,
        prefix: str | None = None,
    ) -> "CnpjGeneratorOptions":
        """Creates a new instance of CnpjGeneratorOptions with the given options merged with the current options."""
        kwargs = {}

        if format is not None:
            kwargs["format"] = format
        if prefix is not None:
            kwargs["prefix"] = prefix

        return replace(self, **kwargs)

    def __setattr__(self, name: str, value: object) -> None:
        if name == "prefix" and value is not None:
            max_digits = CNPJ_LENGTH - 2
            value = re.sub(r"[^0-9]", "", str(value))
            prefix_length = len(value)

            if prefix_length > CNPJ_LENGTH - 2:
                raise CnpjGeneratorInvalidPrefixLengthError(prefix_length, max_digits)

            if prefix_length > 8 and value[8:] == "0000":
                raise CnpjGeneratorInvalidPrefixBranchIdError(value[8:])

        object.__setattr__(self, name, value)
