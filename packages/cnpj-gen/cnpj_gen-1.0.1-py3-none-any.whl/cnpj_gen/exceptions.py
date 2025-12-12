class CnpjGeneratorError(Exception):
    """Base exception for all cnpj-gen related errors."""


class CnpjGeneratorInvalidPrefixLengthError(CnpjGeneratorError):
    """Raised when the prefix length is too long."""

    def __init__(self, prefix_length: int, max_length: int) -> None:
        self.prefix_length = prefix_length
        self.max_length = max_length

        super().__init__(
            f"The prefix length must be less than or equal to {max_length}. Got {prefix_length}."
        )


class CnpjGeneratorInvalidPrefixBranchIdError(CnpjGeneratorError):
    """Raised when the prefix branch ID is invalid."""

    def __init__(self, prefix_branch_id: str) -> None:
        self.prefix_branch_id = prefix_branch_id

        super().__init__(f'The prefix branch ID "{prefix_branch_id}" is not valid.')
