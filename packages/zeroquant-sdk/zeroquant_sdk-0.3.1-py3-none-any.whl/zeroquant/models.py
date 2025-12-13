# packages/python-sdk/zeroquant/models.py
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional

class VaultConfig(BaseModel):
    """Configuration for ZeroQuant client."""

    model_config = ConfigDict(frozen=True)

    owner: str = Field(pattern=r'^0x[a-fA-F0-9]{40}$', description="Vault owner address")
    permission_manager: str = Field(pattern=r'^0x[a-fA-F0-9]{40}$', description="PermissionManager contract address")
    factory_address: str = Field(pattern=r'^0x[a-fA-F0-9]{40}$', description="UVAFactory contract address")
    swap_intent_address: Optional[str] = Field(None, pattern=r'^0x[a-fA-F0-9]{40}$', description="SwapIntent contract address")


class SwapParams(BaseModel):
    """Parameters for token swap operation."""

    amount_in: int = Field(gt=0, description="Amount of input token in wei")
    amount_out_min: int = Field(gt=0, description="Minimum output amount in wei")
    path: List[str] = Field(min_length=2, description="Token swap path")
    to: str = Field(pattern=r'^0x[a-fA-F0-9]{40}$', description="Recipient address")
    deadline: int = Field(gt=0, description="Transaction deadline (unix timestamp)")

    @field_validator('path')
    @classmethod
    def validate_addresses(cls, v: List[str]) -> List[str]:
        for addr in v:
            if not addr.startswith('0x') or len(addr) != 42:
                raise ValueError(f"Invalid address in path: {addr}")
        return v


class ExecuteParams(BaseModel):
    """Parameters for vault execute operation."""

    target: str = Field(pattern=r'^0x[a-fA-F0-9]{40}$', description="Target contract address")
    value: int = Field(ge=0, description="ETH value to send in wei")
    data: bytes = Field(description="Encoded calldata")


class ExecuteBatchParams(BaseModel):
    """Parameters for batch execution."""

    targets: List[str] = Field(min_length=1, description="Target contract addresses")
    values: List[int] = Field(min_length=1, description="ETH values in wei")
    calldatas: List[bytes] = Field(min_length=1, description="Encoded calldatas")

    @field_validator('targets')
    @classmethod
    def validate_targets(cls, v: List[str]) -> List[str]:
        for addr in v:
            if not addr.startswith('0x') or len(addr) != 42:
                raise ValueError(f"Invalid target address: {addr}")
        return v

    def model_post_init(self, __context) -> None:
        """Validate that all arrays have the same length."""
        if not (len(self.targets) == len(self.values) == len(self.calldatas)):
            raise ValueError("targets, values, and calldatas must have the same length")


class TransactionResult(BaseModel):
    """Result of a transaction."""

    tx_hash: str = Field(description="Transaction hash")
    block_number: int = Field(description="Block number")
    gas_used: int = Field(description="Gas used")
    status: int = Field(description="Transaction status (1=success, 0=failure)")
    logs: List[dict] = Field(default_factory=list, description="Event logs")


class GasEstimate(BaseModel):
    """Gas estimation result."""

    gas_limit: int = Field(description="Estimated gas limit with buffer")
    gas_price: int = Field(description="Current gas price in wei")
    max_fee_per_gas: Optional[int] = Field(None, description="Max fee per gas (EIP-1559)")
    max_priority_fee_per_gas: Optional[int] = Field(None, description="Max priority fee (EIP-1559)")
    estimated_cost_wei: int = Field(description="Estimated total cost in wei")
    estimated_cost_eth: str = Field(description="Estimated total cost in ETH")


class AgentSession(BaseModel):
    """Agent session with permissions and limits."""

    agent: str = Field(pattern=r'^0x[a-fA-F0-9]{40}$', description="Agent address")
    expires_at: int = Field(description="Session expiration timestamp")
    daily_limit_usd: int = Field(description="Daily spending limit in USD")
    per_tx_limit_usd: int = Field(description="Per-transaction limit in USD")
    max_position_size_pct: int = Field(description="Maximum position size percentage")
    max_slippage_bps: int = Field(description="Maximum slippage in basis points")
    max_leverage: int = Field(description="Maximum leverage")
    allowed_operations: List[str] = Field(description="Allowed operation signatures (bytes4)")
    allowed_protocols: List[str] = Field(description="Allowed protocol addresses")
    daily_spent_usd: int = Field(default=0, description="Amount spent today in USD")
    last_reset_timestamp: int = Field(default=0, description="Last daily limit reset")


class CreateSessionParams(BaseModel):
    """Parameters for creating an agent session."""

    agent: str = Field(pattern=r'^0x[a-fA-F0-9]{40}$', description="Agent address")
    expires_at: int = Field(description="Session expiration timestamp")
    daily_limit_usd: int = Field(ge=0, description="Daily spending limit in USD")
    per_tx_limit_usd: int = Field(ge=0, description="Per-transaction limit in USD")
    max_position_size_pct: int = Field(ge=0, le=100, description="Maximum position size percentage")
    max_slippage_bps: int = Field(ge=0, le=10000, description="Maximum slippage in basis points")
    max_leverage: int = Field(ge=1, description="Maximum leverage")
    allowed_operations: List[str] = Field(description="Allowed operation signatures (bytes4)")
    allowed_protocols: List[str] = Field(description="Allowed protocol addresses")

    @field_validator('allowed_operations')
    @classmethod
    def validate_operations(cls, v: List[str]) -> List[str]:
        for op in v:
            if not op.startswith('0x') or len(op) != 10:
                raise ValueError(f"Invalid operation signature (must be bytes4): {op}")
        return v

    @field_validator('allowed_protocols')
    @classmethod
    def validate_protocols(cls, v: List[str]) -> List[str]:
        for addr in v:
            if not addr.startswith('0x') or len(addr) != 42:
                raise ValueError(f"Invalid protocol address: {addr}")
        return v
