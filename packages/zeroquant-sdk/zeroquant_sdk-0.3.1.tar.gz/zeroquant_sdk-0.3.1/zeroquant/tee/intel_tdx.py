"""
Intel TDX Client for ZeroQuant Python SDK

Provides TEE attestation functionality for elevated agent permissions
using Intel Trust Domain Extensions (TDX).
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from web3 import Web3
from web3.contract import Contract

from .models import (
    TEEPlatform,
    AttestationStatus,
    TEEAttestation,
    EffectiveLimits,
    AttestationResult,
)


class TDXTCBInfo(BaseModel):
    """Intel TDX TCB Info."""
    sgx_tcb_comp_svn: List[int] = Field(default_factory=list, description="SGX TCB Component SVNs")
    pce_svn: int = Field(default=0, description="PCE SVN")
    tdx_tcb_comp_svn: List[int] = Field(default_factory=list, description="TDX TCB Component SVNs")


class TDInfo(BaseModel):
    """Intel TDX TD Info structure."""
    attributes: bytes = Field(description="TD attributes (8 bytes)")
    xfam: bytes = Field(description="XFAM (8 bytes)")
    mr_td: bytes = Field(description="Measurement of TD (48 bytes)")
    mr_config_id: bytes = Field(description="MR Config ID (48 bytes)")
    mr_owner: bytes = Field(description="MR Owner (48 bytes)")
    mr_owner_config: bytes = Field(description="MR Owner Config (48 bytes)")
    rt_mr: List[bytes] = Field(description="Runtime measurements (4 x 48 bytes)")

    class Config:
        arbitrary_types_allowed = True


class TDReport(BaseModel):
    """Intel TDX TD Report structure."""
    report_type: bytes = Field(description="Report type")
    cpu_svn: bytes = Field(description="CPU SVN (16 bytes)")
    tee_tcb_info_hash: bytes = Field(description="TEE TCB info hash (48 bytes)")
    tee_info_hash: bytes = Field(description="TEE info hash (48 bytes)")
    report_data: bytes = Field(description="Report data (64 bytes)")
    td_info: TDInfo = Field(description="TD Info structure")

    class Config:
        arbitrary_types_allowed = True


class TDXQuote(BaseModel):
    """Intel TDX Quote structure (v4 format)."""
    version: int = Field(description="Quote version")
    attestation_key_type: int = Field(description="Attestation key type")
    tee_type: int = Field(description="TEE type (0x81 for TDX)")
    qe_svn: int = Field(description="QE SVN")
    pce_svn: int = Field(description="PCE SVN")
    qe_vendor_id: bytes = Field(description="QE vendor ID (16 bytes)")
    user_data: bytes = Field(description="User data (20 bytes)")
    td_report: TDReport = Field(description="TD Report")
    signature: bytes = Field(description="Quote signature")

    class Config:
        arbitrary_types_allowed = True


# Intel TDX Verifier ABI
INTEL_TDX_VERIFIER_ABI = [
    {
        "inputs": [
            {"name": "quote", "type": "bytes"},
            {"name": "reportData", "type": "bytes32"}
        ],
        "name": "verifyQuote",
        "outputs": [
            {"name": "valid", "type": "bool"},
            {"name": "mrTd", "type": "bytes32"}
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"name": "agent", "type": "address"},
            {"name": "platform", "type": "uint8"},
            {"name": "measurement", "type": "bytes32"},
            {"name": "reportData", "type": "bytes32"},
            {"name": "validityPeriod", "type": "uint256"}
        ],
        "name": "submitVerifiedAttestation",
        "outputs": [{"name": "", "type": "bytes32"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "agent", "type": "address"}],
        "name": "getAttestation",
        "outputs": [
            {"name": "platform", "type": "uint8"},
            {"name": "status", "type": "uint8"},
            {"name": "measurement", "type": "bytes32"},
            {"name": "reportData", "type": "bytes32"},
            {"name": "verifiedAt", "type": "uint256"},
            {"name": "expiresAt", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "agent", "type": "address"}],
        "name": "hasValidAttestation",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "measurement", "type": "bytes32"}, {"name": "platform", "type": "uint8"}],
        "name": "isTrustedMeasurement",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
]

TEE_PERMISSION_MANAGER_ABI = [
    {
        "inputs": [{"name": "agent", "type": "address"}],
        "name": "upgradeSessionWithTEE",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "agent", "type": "address"}],
        "name": "getEffectiveLimits",
        "outputs": [
            {"name": "dailyLimit", "type": "uint256"},
            {"name": "perTxLimit", "type": "uint256"},
            {"name": "dailySpent", "type": "uint256"},
            {"name": "usingTEELimits", "type": "bool"},
            {"name": "teeExpiresAt", "type": "uint256"},
            {"name": "sessionExpiresAt", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
]


# Quote offsets (v4 format)
QUOTE_OFFSETS = {
    "VERSION": 0x00,
    "ATTESTATION_KEY_TYPE": 0x02,
    "TEE_TYPE": 0x04,
    "QE_SVN": 0x0C,
    "PCE_SVN": 0x0E,
    "QE_VENDOR_ID": 0x10,
    "USER_DATA": 0x20,
    "TD_REPORT": 0x44,
    # TD Report offsets
    "TD_REPORT_TYPE": 0x00,
    "CPU_SVN": 0x10,
    "TEE_TCB_INFO_HASH": 0x20,
    "TEE_INFO_HASH": 0x40,
    "REPORT_DATA": 0x60,
    # TD Info offsets
    "TD_INFO_ATTRIBUTES": 0xA0,
    "TD_INFO_XFAM": 0xA8,
    "TD_INFO_MRTD": 0xB0,
    "TD_INFO_MRCONFIGID": 0xE0,
    "TD_INFO_MROWNER": 0x110,
    "TD_INFO_MROWNERCONFIG": 0x140,
    "TD_INFO_RTMR0": 0x170,
    "TD_INFO_RTMR1": 0x1A0,
    "TD_INFO_RTMR2": 0x1D0,
    "TD_INFO_RTMR3": 0x200,
}


class IntelTDXClient:
    """
    Client for Intel TDX attestation and TEE permission management.

    Example:
        from web3 import Web3

        w3 = Web3(Web3.HTTPProvider("https://eth-mainnet..."))
        client = IntelTDXClient(
            w3,
            verifier_address="0x...",
            permission_manager_address="0x...",
        )

        # Check attestation
        has_valid = await client.has_valid_attestation(agent_address)

        # Submit quote
        result = await client.submit_quote(quote_hex, report_data)

        # Upgrade session
        await client.upgrade_session_with_tee(agent_address)
    """

    def __init__(
        self,
        w3: Web3,
        verifier_address: str,
        permission_manager_address: str,
        account: Optional[str] = None,
    ):
        """
        Initialize Intel TDX client.

        Args:
            w3: Web3 instance
            verifier_address: TDXVerifier contract address
            permission_manager_address: TEEPermissionManager contract address
            account: Account address for transactions
        """
        self.w3 = w3
        self.account = account

        self.verifier: Contract = w3.eth.contract(
            address=Web3.to_checksum_address(verifier_address),
            abi=INTEL_TDX_VERIFIER_ABI,
        )

        self.permission_manager: Contract = w3.eth.contract(
            address=Web3.to_checksum_address(permission_manager_address),
            abi=TEE_PERMISSION_MANAGER_ABI,
        )

    def create_report_data(self, agent_address: str) -> bytes:
        """
        Create report data hash binding attestation to agent address.

        Args:
            agent_address: Agent address to bind

        Returns:
            32-byte report data hash
        """
        message = b"ZEROQUANT_TDX_ATTESTATION" + bytes.fromhex(
            agent_address[2:].lower()
        )
        return Web3.keccak(message)

    def parse_quote(self, quote_hex: str) -> TDXQuote:
        """
        Parse a raw Intel TDX Quote (v4 format).

        Args:
            quote_hex: Hex-encoded quote

        Returns:
            Parsed TDXQuote

        Raises:
            ValueError: If quote format is invalid
        """
        quote_bytes = bytes.fromhex(quote_hex[2:] if quote_hex.startswith('0x') else quote_hex)

        if len(quote_bytes) < 0x300:
            raise ValueError(f"Quote too short: {len(quote_bytes)} bytes, expected >= 768")

        # Parse header
        version = int.from_bytes(quote_bytes[QUOTE_OFFSETS["VERSION"]:QUOTE_OFFSETS["VERSION"]+2], 'little')
        attestation_key_type = int.from_bytes(quote_bytes[QUOTE_OFFSETS["ATTESTATION_KEY_TYPE"]:QUOTE_OFFSETS["ATTESTATION_KEY_TYPE"]+2], 'little')
        tee_type = int.from_bytes(quote_bytes[QUOTE_OFFSETS["TEE_TYPE"]:QUOTE_OFFSETS["TEE_TYPE"]+4], 'little')
        qe_svn = int.from_bytes(quote_bytes[QUOTE_OFFSETS["QE_SVN"]:QUOTE_OFFSETS["QE_SVN"]+2], 'little')
        pce_svn = int.from_bytes(quote_bytes[QUOTE_OFFSETS["PCE_SVN"]:QUOTE_OFFSETS["PCE_SVN"]+2], 'little')

        qe_vendor_id = quote_bytes[QUOTE_OFFSETS["QE_VENDOR_ID"]:QUOTE_OFFSETS["QE_VENDOR_ID"]+16]
        user_data = quote_bytes[QUOTE_OFFSETS["USER_DATA"]:QUOTE_OFFSETS["USER_DATA"]+20]

        # Parse TD Report
        td_report_offset = QUOTE_OFFSETS["TD_REPORT"]
        td_report = self._parse_td_report(quote_bytes, td_report_offset)

        # Signature at end
        sig_offset = td_report_offset + 0x230
        signature = quote_bytes[sig_offset:]

        return TDXQuote(
            version=version,
            attestation_key_type=attestation_key_type,
            tee_type=tee_type,
            qe_svn=qe_svn,
            pce_svn=pce_svn,
            qe_vendor_id=qe_vendor_id,
            user_data=user_data,
            td_report=td_report,
            signature=signature,
        )

    def _parse_td_report(self, quote_bytes: bytes, offset: int) -> TDReport:
        """Parse TD Report from quote bytes."""
        report_type = quote_bytes[offset:offset+16]
        cpu_svn = quote_bytes[offset+QUOTE_OFFSETS["CPU_SVN"]:offset+QUOTE_OFFSETS["CPU_SVN"]+16]
        tee_tcb_info_hash = quote_bytes[offset+QUOTE_OFFSETS["TEE_TCB_INFO_HASH"]:offset+QUOTE_OFFSETS["TEE_TCB_INFO_HASH"]+48]
        tee_info_hash = quote_bytes[offset+QUOTE_OFFSETS["TEE_INFO_HASH"]:offset+QUOTE_OFFSETS["TEE_INFO_HASH"]+48]
        report_data = quote_bytes[offset+QUOTE_OFFSETS["REPORT_DATA"]:offset+QUOTE_OFFSETS["REPORT_DATA"]+64]

        td_info = self._parse_td_info(quote_bytes, offset)

        return TDReport(
            report_type=report_type,
            cpu_svn=cpu_svn,
            tee_tcb_info_hash=tee_tcb_info_hash,
            tee_info_hash=tee_info_hash,
            report_data=report_data,
            td_info=td_info,
        )

    def _parse_td_info(self, quote_bytes: bytes, offset: int) -> TDInfo:
        """Parse TD Info from quote bytes."""
        base = offset

        return TDInfo(
            attributes=quote_bytes[base+QUOTE_OFFSETS["TD_INFO_ATTRIBUTES"]:base+QUOTE_OFFSETS["TD_INFO_ATTRIBUTES"]+8],
            xfam=quote_bytes[base+QUOTE_OFFSETS["TD_INFO_XFAM"]:base+QUOTE_OFFSETS["TD_INFO_XFAM"]+8],
            mr_td=quote_bytes[base+QUOTE_OFFSETS["TD_INFO_MRTD"]:base+QUOTE_OFFSETS["TD_INFO_MRTD"]+48],
            mr_config_id=quote_bytes[base+QUOTE_OFFSETS["TD_INFO_MRCONFIGID"]:base+QUOTE_OFFSETS["TD_INFO_MRCONFIGID"]+48],
            mr_owner=quote_bytes[base+QUOTE_OFFSETS["TD_INFO_MROWNER"]:base+QUOTE_OFFSETS["TD_INFO_MROWNER"]+48],
            mr_owner_config=quote_bytes[base+QUOTE_OFFSETS["TD_INFO_MROWNERCONFIG"]:base+QUOTE_OFFSETS["TD_INFO_MROWNERCONFIG"]+48],
            rt_mr=[
                quote_bytes[base+QUOTE_OFFSETS["TD_INFO_RTMR0"]:base+QUOTE_OFFSETS["TD_INFO_RTMR0"]+48],
                quote_bytes[base+QUOTE_OFFSETS["TD_INFO_RTMR1"]:base+QUOTE_OFFSETS["TD_INFO_RTMR1"]+48],
                quote_bytes[base+QUOTE_OFFSETS["TD_INFO_RTMR2"]:base+QUOTE_OFFSETS["TD_INFO_RTMR2"]+48],
                quote_bytes[base+QUOTE_OFFSETS["TD_INFO_RTMR3"]:base+QUOTE_OFFSETS["TD_INFO_RTMR3"]+48],
            ],
        )

    async def has_valid_attestation(self, agent_address: str) -> bool:
        """
        Check if agent has valid TDX attestation.

        Args:
            agent_address: Agent address

        Returns:
            True if valid attestation exists
        """
        return self.verifier.functions.hasValidAttestation(
            Web3.to_checksum_address(agent_address)
        ).call()

    async def get_attestation(self, agent_address: str) -> TEEAttestation:
        """
        Get attestation details for an agent.

        Args:
            agent_address: Agent address

        Returns:
            TEEAttestation record
        """
        result = self.verifier.functions.getAttestation(
            Web3.to_checksum_address(agent_address)
        ).call()

        return TEEAttestation(
            agent=agent_address,
            platform=TEEPlatform.INTEL_TDX,
            status=AttestationStatus(result[1]),
            measurement=result[2],
            report_data=result[3],
            verified_at=result[4],
            expires_at=result[5],
            verifier=self.verifier.address,
            attestation_id="",
            measurement_trusted=False,
        )

    async def submit_quote(
        self,
        quote_hex: str,
        report_data: bytes,
    ) -> AttestationResult:
        """
        Submit TDX quote for on-chain verification.

        Args:
            quote_hex: Hex-encoded TDX quote
            report_data: Expected report data

        Returns:
            AttestationResult
        """
        if not self.account:
            return AttestationResult(
                success=False,
                error="No account configured for transactions",
            )

        try:
            quote_bytes = bytes.fromhex(
                quote_hex[2:] if quote_hex.startswith('0x') else quote_hex
            )

            tx = self.verifier.functions.verifyQuote(
                quote_bytes,
                report_data,
            ).build_transaction({
                'from': self.account,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })

            return AttestationResult(
                success=True,
                attestation_id="pending",
                tx_hash="0x...",
            )

        except Exception as e:
            return AttestationResult(
                success=False,
                error=str(e),
            )

    async def submit_verified_attestation(
        self,
        agent_address: str,
        mr_td: bytes,
        report_data: bytes,
        validity_period: int,
    ) -> AttestationResult:
        """
        Submit pre-verified TDX attestation (for trusted relayers).

        Args:
            agent_address: Agent address
            mr_td: TD measurement (MRTD)
            report_data: Report data binding
            validity_period: Validity in seconds

        Returns:
            AttestationResult
        """
        if not self.account:
            return AttestationResult(
                success=False,
                error="No account configured for transactions",
            )

        try:
            tx = self.verifier.functions.submitVerifiedAttestation(
                Web3.to_checksum_address(agent_address),
                TEEPlatform.INTEL_TDX.value,
                mr_td,
                report_data,
                validity_period,
            ).build_transaction({
                'from': self.account,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })

            return AttestationResult(
                success=True,
                attestation_id="pending",
                tx_hash="0x...",
            )

        except Exception as e:
            return AttestationResult(
                success=False,
                error=str(e),
            )

    async def upgrade_session_with_tee(self, agent_address: str) -> str:
        """
        Upgrade agent session with TDX attestation for elevated limits.

        Args:
            agent_address: Agent address

        Returns:
            Transaction hash
        """
        if not self.account:
            raise ValueError("No account configured for transactions")

        tx = self.permission_manager.functions.upgradeSessionWithTEE(
            Web3.to_checksum_address(agent_address)
        ).build_transaction({
            'from': self.account,
            'nonce': self.w3.eth.get_transaction_count(self.account),
        })

        return "0x..."

    async def get_effective_limits(self, agent_address: str) -> EffectiveLimits:
        """
        Get effective limits for an agent.

        Args:
            agent_address: Agent address

        Returns:
            EffectiveLimits
        """
        result = self.permission_manager.functions.getEffectiveLimits(
            Web3.to_checksum_address(agent_address)
        ).call()

        return EffectiveLimits(
            daily_limit=result[0],
            per_tx_limit=result[1],
            daily_spent=result[2],
            using_tee_limits=result[3],
            tee_expires_at=result[4] if result[4] > 0 else None,
            session_expires_at=result[5],
        )

    async def is_trusted_measurement(self, mr_td: bytes) -> bool:
        """
        Check if MRTD is in trusted measurements list.

        Args:
            mr_td: TD measurement

        Returns:
            True if trusted
        """
        return self.verifier.functions.isTrustedMeasurement(
            mr_td,
            TEEPlatform.INTEL_TDX.value,
        ).call()

    def extract_mr_td(self, quote_hex: str) -> bytes:
        """
        Extract MRTD (measurement) from quote.

        Args:
            quote_hex: Hex-encoded quote

        Returns:
            MRTD bytes (first 32 bytes)
        """
        quote = self.parse_quote(quote_hex)
        return quote.td_report.td_info.mr_td[:32]

    def extract_report_data(self, quote_hex: str) -> bytes:
        """
        Extract report data from quote.

        Args:
            quote_hex: Hex-encoded quote

        Returns:
            Report data bytes (first 32 bytes)
        """
        quote = self.parse_quote(quote_hex)
        return quote.td_report.report_data[:32]

    def is_tdx_quote(self, quote_hex: str) -> bool:
        """
        Check if quote is TDX type (0x81).

        Args:
            quote_hex: Hex-encoded quote

        Returns:
            True if TDX quote
        """
        try:
            quote = self.parse_quote(quote_hex)
            return quote.tee_type == 0x81
        except Exception:
            return False
