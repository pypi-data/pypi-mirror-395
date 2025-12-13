"""Custom exceptions for ZeroQuant SDK."""


class ZeroQuantError(Exception):
    """Base exception for all ZeroQuant errors."""
    pass


class NotConnectedError(ZeroQuantError):
    """Raised when attempting operations without connecting to a vault."""
    pass


class ReadOnlyError(ZeroQuantError):
    """Raised when attempting write operations in read-only mode."""
    pass


class ValidationError(ZeroQuantError):
    """Raised when input validation fails."""
    pass


class TransactionError(ZeroQuantError):
    """Raised when a transaction fails."""

    def __init__(self, message: str, tx_hash: str = None):
        super().__init__(message)
        self.tx_hash = tx_hash


class ContractError(ZeroQuantError):
    """Raised when a contract call fails."""

    def __init__(self, message: str, revert_reason: str = None):
        super().__init__(message)
        self.revert_reason = revert_reason
