# packages/python-sdk/tests/test_models.py
import pytest
from zeroquant.models import VaultConfig, SwapParams, ExecuteParams

def test_vault_config_validation():
    # Valid config
    config = VaultConfig(
        owner="0x" + "a" * 40,
        permission_manager="0x" + "b" * 40,
        factory_address="0x" + "c" * 40
    )
    assert config.owner.startswith("0x")

    # Invalid: bad address format
    with pytest.raises(ValueError):
        VaultConfig(
            owner="invalid",
            permission_manager="0x" + "b" * 40,
            factory_address="0x" + "c" * 40
        )

def test_swap_params_validation():
    # Valid params
    params = SwapParams(
        amount_in=1000000,
        amount_out_min=900000,
        path=["0x" + "a" * 40, "0x" + "b" * 40],
        to="0x" + "c" * 40,
        deadline=1234567890
    )
    assert len(params.path) == 2

    # Invalid: negative amount
    with pytest.raises(ValueError):
        SwapParams(
            amount_in=-1,
            amount_out_min=900000,
            path=["0x" + "a" * 40, "0x" + "b" * 40],
            to="0x" + "c" * 40,
            deadline=1234567890
        )

    # Invalid: path too short
    with pytest.raises(ValueError):
        SwapParams(
            amount_in=1000000,
            amount_out_min=900000,
            path=["0x" + "a" * 40],
            to="0x" + "c" * 40,
            deadline=1234567890
        )
