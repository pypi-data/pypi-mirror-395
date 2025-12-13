"""Base exception classes for SpecMem.

All SpecMem exceptions inherit from SpecMemError, providing consistent
error handling with error codes and optional details.
"""

from typing import Any


class SpecMemError(Exception):
    """Base exception for all SpecMem errors.

    Attributes:
        message: Human-readable error description
        code: Machine-readable error code for programmatic handling
        details: Optional dictionary with additional error context
    """

    def __init__(
        self,
        message: str,
        code: str = "SPECMEM_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class AdapterError(SpecMemError):
    """Raised when a spec adapter encounters an error.

    Examples:
        - Malformed spec files
        - Missing required files
        - Parse failures
    """

    def __init__(
        self,
        message: str,
        code: str = "ADAPTER_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code, details)


class VectorStoreError(SpecMemError):
    """Raised when vector storage operations fail.

    Examples:
        - Connection failures
        - Schema issues
        - Query failures
    """

    def __init__(
        self,
        message: str,
        code: str = "VECTORSTORE_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code, details)


class ConfigurationError(SpecMemError):
    """Raised when configuration is invalid.

    Examples:
        - Invalid config values
        - Missing required fields
        - Unsupported backend specified
    """

    def __init__(
        self,
        message: str,
        code: str = "CONFIG_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code, details)


class EmbeddingError(SpecMemError):
    """Raised when embedding generation fails.

    Examples:
        - Provider unavailable
        - Rate limits exceeded
        - Invalid input text
    """

    def __init__(
        self,
        message: str,
        code: str = "EMBEDDING_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, code, details)


class LifecycleError(SpecMemError):
    """Raised when an invalid lifecycle state transition is attempted.

    Examples:
        - Transitioning from obsolete (terminal state)
        - Skipping required intermediate states
    """

    def __init__(
        self,
        message: str,
        from_status: str,
        to_status: str,
        block_id: str,
        valid_transitions: list[str] | None = None,
    ) -> None:
        details = {
            "from_status": from_status,
            "to_status": to_status,
            "block_id": block_id,
            "valid_transitions": valid_transitions or [],
        }
        super().__init__(message, code="LIFECYCLE_ERROR", details=details)
        self.from_status = from_status
        self.to_status = to_status
        self.block_id = block_id
