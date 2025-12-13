from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.contract import AsyncContract
from eth_account import Account
from typing import Optional, List, Callable, Any
import time
import asyncio

from .models import (
    VaultConfig,
    ExecuteParams,
    ExecuteBatchParams,
    TransactionResult,
    GasEstimate,
    AgentSession,
    CreateSessionParams,
)
from .exceptions import ReadOnlyError, NotConnectedError, TransactionError
from .abis import UVA_FACTORY_ABI, UVA_ACCOUNT_ABI, PERMISSION_MANAGER_ABI


class ZeroQuantClient:
    """
    Async-first client for ZeroQuant vault operations.

    Supports three authentication modes:
    1. Agent wallet (private_key)
    2. Delegated signing (session_key + delegation_proof)
    3. API key (api_key + api_url)
    """

    def __init__(
        self,
        provider: str | AsyncWeb3,
        config: VaultConfig,
        private_key: Optional[str] = None,
        session_key: Optional[str] = None,
        delegation_proof: Optional[str] = None,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None
    ):
        # Setup Web3
        if isinstance(provider, str):
            self.w3 = AsyncWeb3(AsyncHTTPProvider(provider))
        else:
            self.w3 = provider

        self.config = config
        self.vault: Optional[AsyncContract] = None

        # Authentication mode selection
        if private_key:
            self.account = Account.from_key(private_key)
            self.auth_mode = "wallet"
        elif session_key and delegation_proof:
            self.account = Account.from_key(session_key)
            self.delegation = delegation_proof
            self.auth_mode = "delegated"
        elif api_key and api_url:
            self.api_key = api_key
            self.api_url = api_url
            self.account = None
            self.auth_mode = "api"
        else:
            # Read-only mode
            self.account = None
            self.auth_mode = "readonly"

    async def create_vault(self, salt: int) -> str:
        """Creates a new vault with deterministic address."""
        if self.auth_mode == "readonly":
            raise ReadOnlyError("Signer required to create vault")

        factory = self.w3.eth.contract(
            address=self.config.factory_address,
            abi=UVA_FACTORY_ABI
        )

        # Estimate gas dynamically
        gas_estimate = await factory.functions.createAccount(
            self.config.owner,
            salt
        ).estimate_gas({'from': self.account.address})

        # Apply 20% buffer
        gas_limit = int(gas_estimate * 1.2)

        # Build transaction
        tx = await factory.functions.createAccount(
            self.config.owner,
            salt
        ).build_transaction({
            'from': self.account.address,
            'nonce': await self.w3.eth.get_transaction_count(self.account.address),
            'gas': gas_limit,
            'gasPrice': await self.w3.eth.gas_price
        })

        # Sign and send
        signed = self.account.sign_transaction(tx)
        tx_hash = await self.w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = await self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] != 1:
            raise TransactionError("Vault creation failed", tx_hash.hex())

        # Parse AccountCreated event
        logs = factory.events.AccountCreated().process_receipt(receipt)
        vault_address = logs[0]['args']['account']

        await self.connect_vault(vault_address)

        return vault_address

    async def connect_vault(self, vault_address: str) -> None:
        """Connects to an existing vault."""
        self.vault = self.w3.eth.contract(
            address=vault_address,
            abi=UVA_ACCOUNT_ABI
        )

    async def execute(
        self,
        target: str,
        value: int,
        data: bytes
    ) -> TransactionResult:
        """Executes a single operation through the vault."""
        if not self.vault:
            raise NotConnectedError("Must connect to vault first using connect_vault()")

        if self.auth_mode == "readonly":
            raise ReadOnlyError("Signer required for execution")

        # Estimate gas dynamically
        gas_estimate = await self.vault.functions.execute(
            target,
            value,
            data
        ).estimate_gas({'from': self.account.address})

        # Apply 20% buffer
        gas_limit = int(gas_estimate * 1.2)

        # Build transaction
        tx = await self.vault.functions.execute(
            target,
            value,
            data
        ).build_transaction({
            'from': self.account.address,
            'nonce': await self.w3.eth.get_transaction_count(self.account.address),
            'gas': gas_limit,
            'gasPrice': await self.w3.eth.gas_price
        })

        # Sign and send
        signed = self.account.sign_transaction(tx)
        tx_hash = await self.w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = await self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] != 1:
            raise TransactionError("Execution failed", tx_hash.hex())

        return TransactionResult(
            tx_hash=tx_hash.hex(),
            block_number=receipt['blockNumber'],
            gas_used=receipt['gasUsed'],
            status=receipt['status'],
            logs=[dict(log) for log in receipt['logs']]
        )

    async def execute_batch(
        self,
        targets: List[str],
        values: List[int],
        calldatas: List[bytes]
    ) -> TransactionResult:
        """Executes multiple operations atomically."""
        if not self.vault:
            raise NotConnectedError("Must connect to vault first")

        if self.auth_mode == "readonly":
            raise ReadOnlyError("Signer required for execution")

        # Estimate gas dynamically
        gas_estimate = await self.vault.functions.executeBatch(
            targets,
            values,
            calldatas
        ).estimate_gas({'from': self.account.address})

        # Apply 20% buffer
        gas_limit = int(gas_estimate * 1.2)

        tx = await self.vault.functions.executeBatch(
            targets,
            values,
            calldatas
        ).build_transaction({
            'from': self.account.address,
            'nonce': await self.w3.eth.get_transaction_count(self.account.address),
            'gas': gas_limit,
            'gasPrice': await self.w3.eth.gas_price
        })

        signed = self.account.sign_transaction(tx)
        tx_hash = await self.w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = await self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] != 1:
            raise TransactionError("Batch execution failed", tx_hash.hex())

        return TransactionResult(
            tx_hash=tx_hash.hex(),
            block_number=receipt['blockNumber'],
            gas_used=receipt['gasUsed'],
            status=receipt['status'],
            logs=[dict(log) for log in receipt['logs']]
        )

    async def get_balance(self) -> int:
        """Gets vault ETH balance in wei."""
        if not self.vault:
            raise NotConnectedError("Must connect to vault first")

        return await self.w3.eth.get_balance(self.vault.address)

    async def get_owner(self) -> str:
        """Gets vault owner address."""
        if not self.vault:
            raise NotConnectedError("Must connect to vault first")

        return await self.vault.functions.owner().call()

    async def estimate_execute(self, target: str, value: int, data: bytes) -> GasEstimate:
        """Estimates gas for a single execute operation."""
        if not self.vault:
            raise NotConnectedError("Must connect to vault first")

        # Get sender address (use zero address for read-only mode)
        sender = self.account.address if self.account else "0x0000000000000000000000000000000000000000"

        # Estimate gas
        gas_estimate = await self.vault.functions.execute(
            target, value, data
        ).estimate_gas({'from': sender})

        # Apply 20% buffer
        gas_limit = int(gas_estimate * 1.2)

        # Get gas price
        gas_price = await self.w3.eth.gas_price

        # Calculate estimated cost
        estimated_cost_wei = gas_limit * gas_price
        estimated_cost_eth = str(self.w3.from_wei(estimated_cost_wei, 'ether'))

        return GasEstimate(
            gas_limit=gas_limit,
            gas_price=gas_price,
            estimated_cost_wei=estimated_cost_wei,
            estimated_cost_eth=estimated_cost_eth
        )

    async def estimate_batch(
        self,
        targets: List[str],
        values: List[int],
        calldatas: List[bytes]
    ) -> GasEstimate:
        """Estimates gas for a batch execute operation."""
        if not self.vault:
            raise NotConnectedError("Must connect to vault first")

        sender = self.account.address if self.account else "0x0000000000000000000000000000000000000000"

        gas_estimate = await self.vault.functions.executeBatch(
            targets, values, calldatas
        ).estimate_gas({'from': sender})

        gas_limit = int(gas_estimate * 1.2)
        gas_price = await self.w3.eth.gas_price
        estimated_cost_wei = gas_limit * gas_price
        estimated_cost_eth = str(self.w3.from_wei(estimated_cost_wei, 'ether'))

        return GasEstimate(
            gas_limit=gas_limit,
            gas_price=gas_price,
            estimated_cost_wei=estimated_cost_wei,
            estimated_cost_eth=estimated_cost_eth
        )

    # ============================================
    # Session Management
    # ============================================

    async def create_session(self, params: CreateSessionParams) -> TransactionResult:
        """Creates a new agent session with spending limits and permissions."""
        if self.auth_mode == "readonly":
            raise ReadOnlyError("Signer required to create session")

        permission_manager = self.w3.eth.contract(
            address=self.config.permission_manager,
            abi=PERMISSION_MANAGER_ABI
        )

        # Estimate gas
        gas_estimate = await permission_manager.functions.createSession(
            params.agent,
            params.expires_at,
            params.daily_limit_usd,
            params.per_tx_limit_usd,
            params.max_position_size_pct,
            params.max_slippage_bps,
            params.max_leverage,
            params.allowed_operations,
            params.allowed_protocols
        ).estimate_gas({'from': self.account.address})

        gas_limit = int(gas_estimate * 1.2)

        tx = await permission_manager.functions.createSession(
            params.agent,
            params.expires_at,
            params.daily_limit_usd,
            params.per_tx_limit_usd,
            params.max_position_size_pct,
            params.max_slippage_bps,
            params.max_leverage,
            params.allowed_operations,
            params.allowed_protocols
        ).build_transaction({
            'from': self.account.address,
            'nonce': await self.w3.eth.get_transaction_count(self.account.address),
            'gas': gas_limit,
            'gasPrice': await self.w3.eth.gas_price
        })

        signed = self.account.sign_transaction(tx)
        tx_hash = await self.w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = await self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] != 1:
            raise TransactionError("Session creation failed", tx_hash.hex())

        return TransactionResult(
            tx_hash=tx_hash.hex(),
            block_number=receipt['blockNumber'],
            gas_used=receipt['gasUsed'],
            status=receipt['status'],
            logs=[dict(log) for log in receipt['logs']]
        )

    async def has_active_session(self, agent: str) -> bool:
        """Checks if an agent has an active (non-expired) session."""
        permission_manager = self.w3.eth.contract(
            address=self.config.permission_manager,
            abi=PERMISSION_MANAGER_ABI
        )

        return await permission_manager.functions.hasActiveSession(agent).call()

    async def get_session(self, agent: str) -> Optional[AgentSession]:
        """Gets full session details for an agent. Returns None if no session exists."""
        permission_manager = self.w3.eth.contract(
            address=self.config.permission_manager,
            abi=PERMISSION_MANAGER_ABI
        )

        session = await permission_manager.functions.sessions(agent).call()

        # Check if session exists (agent address will be zero if not)
        zero_address = "0x0000000000000000000000000000000000000000"
        if session[0] == zero_address:
            return None

        return AgentSession(
            agent=session[0],
            expires_at=session[1],
            daily_limit_usd=session[2],
            per_tx_limit_usd=session[3],
            max_position_size_pct=session[4],
            max_slippage_bps=session[5],
            max_leverage=session[6],
            daily_spent_usd=session[7],
            last_reset_timestamp=session[8],
            allowed_operations=[],  # Not returned by sessions() mapping
            allowed_protocols=[]    # Not returned by sessions() mapping
        )

    async def revoke_session(self, agent: str) -> TransactionResult:
        """Revokes an agent's session."""
        if self.auth_mode == "readonly":
            raise ReadOnlyError("Signer required to revoke session")

        permission_manager = self.w3.eth.contract(
            address=self.config.permission_manager,
            abi=PERMISSION_MANAGER_ABI
        )

        gas_estimate = await permission_manager.functions.revokeSession(
            agent
        ).estimate_gas({'from': self.account.address})

        gas_limit = int(gas_estimate * 1.2)

        tx = await permission_manager.functions.revokeSession(
            agent
        ).build_transaction({
            'from': self.account.address,
            'nonce': await self.w3.eth.get_transaction_count(self.account.address),
            'gas': gas_limit,
            'gasPrice': await self.w3.eth.gas_price
        })

        signed = self.account.sign_transaction(tx)
        tx_hash = await self.w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = await self.w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt['status'] != 1:
            raise TransactionError("Session revocation failed", tx_hash.hex())

        return TransactionResult(
            tx_hash=tx_hash.hex(),
            block_number=receipt['blockNumber'],
            gas_used=receipt['gasUsed'],
            status=receipt['status'],
            logs=[dict(log) for log in receipt['logs']]
        )

    # ============================================
    # Event Subscription
    # ============================================

    async def on_operation(
        self,
        callback: Callable[[dict], Any],
        poll_interval: float = 2.0
    ) -> Callable[[], None]:
        """
        Subscribe to OperationExecuted events from the vault.

        Args:
            callback: Async function called for each operation event
            poll_interval: Seconds between polling for new events

        Returns:
            Stop function to cancel the subscription
        """
        if not self.vault:
            raise NotConnectedError("Must connect to vault first")

        running = True
        last_block = await self.w3.eth.block_number

        async def poll_events():
            nonlocal last_block
            while running:
                try:
                    current_block = await self.w3.eth.block_number
                    if current_block > last_block:
                        # Get logs for OperationExecuted event
                        logs = await self.w3.eth.get_logs({
                            'address': self.vault.address,
                            'fromBlock': last_block + 1,
                            'toBlock': current_block,
                        })

                        for log in logs:
                            # Parse log and call callback
                            try:
                                await callback({
                                    'tx_hash': log['transactionHash'].hex(),
                                    'block_number': log['blockNumber'],
                                    'data': log['data'],
                                    'topics': [t.hex() for t in log['topics']]
                                })
                            except Exception:
                                pass  # Ignore callback errors

                        last_block = current_block

                    await asyncio.sleep(poll_interval)
                except Exception:
                    await asyncio.sleep(poll_interval)

        # Start polling in background
        task = asyncio.create_task(poll_events())

        def stop():
            nonlocal running
            running = False
            task.cancel()

        return stop

    async def get_vault_address(self) -> Optional[str]:
        """Gets the connected vault address."""
        if not self.vault:
            return None
        return self.vault.address

    async def get_account_address(self, owner: str, salt: int) -> str:
        """
        Gets the deterministic address for a vault given owner and salt.
        This computes the address without deploying the vault.
        """
        factory = self.w3.eth.contract(
            address=self.config.factory_address,
            abi=UVA_FACTORY_ABI
        )

        return await factory.functions.getAccountAddress(owner, salt).call()
