from web3 import Web3
from typing import List
import time

from ..models import SwapParams, ExecuteParams
from ..abis import SWAP_INTENT_ABI


class SwapIntent:
    """Helper for building swap operations."""

    def __init__(self, swap_intent_address: str):
        self.w3 = Web3()
        self.address = self.w3.to_checksum_address(swap_intent_address)
        self.contract = self.w3.eth.contract(address=self.address, abi=SWAP_INTENT_ABI)

    def calculate_min_output(self, expected_output: int, slippage_bps: int) -> int:
        """
        Calculates minimum output with slippage tolerance.

        Args:
            expected_output: Expected amount out in wei
            slippage_bps: Slippage in basis points (50 = 0.5%)

        Returns:
            Minimum acceptable output amount
        """
        return expected_output * (10000 - slippage_bps) // 10000

    def build_calldata(
        self,
        amount_in: int,
        amount_out_min: int,
        path: List[str],
        to: str,
        deadline: int
    ) -> bytes:
        """Encodes swap parameters as calldata."""
        checksummed_path = [self.w3.to_checksum_address(addr) for addr in path]
        checksummed_to = self.w3.to_checksum_address(to)
        encoded = self.contract.functions.executeSwap(
            amount_in, amount_out_min, checksummed_path, checksummed_to, deadline
        )._encode_transaction_data()
        # Convert HexBytes to bytes
        return bytes.fromhex(encoded[2:] if encoded.startswith('0x') else encoded)

    def get_deadline(self, seconds_from_now: int = 3600) -> int:
        """Generates deadline timestamp."""
        return int(time.time()) + seconds_from_now

    def build_execute_params(self, params: SwapParams) -> ExecuteParams:
        """Builds ExecuteParams for vault.execute()."""
        calldata = self.build_calldata(
            params.amount_in,
            params.amount_out_min,
            params.path,
            params.to,
            params.deadline
        )

        return ExecuteParams(
            target=self.address,
            value=params.amount_in,
            data=calldata
        )
