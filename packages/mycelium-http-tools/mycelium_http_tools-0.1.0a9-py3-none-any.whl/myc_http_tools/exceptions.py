"""Custom exceptions for mycelium-http-tools."""

from typing import Optional


class MyceliumError(Exception):
    """Base exception for Mycelium HTTP Tools."""

    def __init__(
        self, message: str, code: Optional[str] = None, exp_true: bool = False
    ):
        self.message = message
        self.code = code
        self.exp_true = exp_true
        super().__init__(self.message)


class InsufficientPrivilegesError(MyceliumError):
    """Raised when there are insufficient privileges to perform an action.

    Maps to MYC00019: "Insufficient privileges"
    Reference: https://github.com/LepistaBioinformatics/mycelium/blob/main/core/src/domain/dtos/native_error_codes.rs
    """

    def __init__(
        self, message: str, filtering_state: Optional[list[str]] = None
    ):
        self.filtering_state = filtering_state or []
        super().__init__(message=message, code="MYC00019", exp_true=True)


class InsufficientLicensesError(MyceliumError):
    """Raised when there are insufficient licenses to perform an action.

    Maps to MYC00019: "Insufficient privileges" (shared code for privilege/license issues)
    Reference: https://github.com/LepistaBioinformatics/mycelium/blob/main/core/src/domain/dtos/native_error_codes.rs
    """

    def __init__(
        self, message: str = "Insufficient licenses to perform these action"
    ):
        super().__init__(message=message, code="MYC00019", exp_true=True)


class ProfileDecodingError(MyceliumError):
    """Raised when there is an error decoding or decompressing a profile.

    Maps to MYC00020: "Possible security issue"
    Reference: https://github.com/LepistaBioinformatics/mycelium/blob/main/core/src/domain/dtos/native_error_codes.rs
    """

    def __init__(self, message: str):
        super().__init__(message=message, code="MYC00020", exp_true=False)


class InvalidFilteringConfigurationError(MyceliumError):
    """Raised when there is an invalid configuration during profile filtering.

    Maps to MYC00019: "Insufficient privileges" (shared code for privilege/configuration issues)
    Reference: https://github.com/LepistaBioinformatics/mycelium/blob/main/core/src/domain/dtos/native_error_codes.rs
    """

    def __init__(self, message: str, parameter_name: Optional[str] = None):
        self.parameter_name = parameter_name
        super().__init__(message=message, code="MYC00019", exp_true=False)
