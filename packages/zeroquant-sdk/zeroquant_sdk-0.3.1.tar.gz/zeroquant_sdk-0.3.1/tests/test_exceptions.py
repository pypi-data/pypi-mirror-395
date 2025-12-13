import pytest
from zeroquant.exceptions import (
    ZeroQuantError,
    NotConnectedError,
    ReadOnlyError,
    ValidationError
)

def test_exception_hierarchy():
    # All exceptions inherit from ZeroQuantError
    assert issubclass(NotConnectedError, ZeroQuantError)
    assert issubclass(ReadOnlyError, ZeroQuantError)
    assert issubclass(ValidationError, ZeroQuantError)

def test_exception_messages():
    error = NotConnectedError("Must connect first")
    assert "connect" in str(error).lower()

    error = ReadOnlyError("Signer required")
    assert "signer" in str(error).lower()
