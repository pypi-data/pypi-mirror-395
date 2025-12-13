import pytest
from zeroquant import ZeroQuantClient, VaultConfig, ReadOnlyError
from web3 import AsyncWeb3

@pytest.fixture
def config():
    return VaultConfig(
        owner="0x" + "a" * 40,
        permission_manager="0x" + "b" * 40,
        factory_address="0x" + "c" * 40
    )

def test_client_initialization_with_private_key(config):
    client = ZeroQuantClient(
        provider="http://localhost:8545",
        config=config,
        private_key="0x" + "1" * 64
    )

    assert client.auth_mode == "wallet"
    assert client.account is not None

def test_client_readonly_mode(config):
    client = ZeroQuantClient(
        provider="http://localhost:8545",
        config=config
    )

    assert client.auth_mode == "readonly"
    assert client.account is None

@pytest.mark.asyncio
async def test_create_vault_requires_signer(config):
    client = ZeroQuantClient(
        provider="http://localhost:8545",
        config=config
    )

    with pytest.raises(ReadOnlyError):
        await client.create_vault(123)
