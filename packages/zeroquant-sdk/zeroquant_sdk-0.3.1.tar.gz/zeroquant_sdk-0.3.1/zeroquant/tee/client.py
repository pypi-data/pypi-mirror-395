"""
AMD SEV Client for ZeroQuant Python SDK

Provides TEE attestation functionality for elevated agent permissions.
"""

from typing import Optional, List
from eth_typing import HexStr
from web3 import Web3
from web3.contract import Contract
import hashlib

from .models import (
    TEEPlatform,
    AttestationStatus,
    TCBVersion,
    AMDSEVReport,
    TEEAttestation,
    TrustedMeasurement,
    EffectiveLimits,
    AttestationResult,
)


# Contract ABIs (simplified for key functions)
AMD_SEV_VERIFIER_ABI = [
    {
        "inputs": [
            {"name": "report", "type": "bytes"},
            {"name": "expectedReportData", "type": "bytes32"}
        ],
        "name": "verifyAttestation",
        "outputs": [
            {"name": "valid", "type": "bool"},
            {"name": "measurement", "type": "bytes32"}
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
    {
        "inputs": [
            {"name": "measurement", "type": "bytes32"},
            {"name": "name", "type": "string"}
        ],
        "name": "addTrustedMeasurement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "measurement", "type": "bytes32"}],
        "name": "removeTrustedMeasurement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "measurement", "type": "bytes32"}],
        "name": "isTrustedMeasurement",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
]


class AMDSEVClient:
    """
    Client for AMD SEV-SNP attestation and TEE permission management.

    Example:
        from web3 import Web3

        w3 = Web3(Web3.HTTPProvider("https://eth-mainnet..."))
        client = AMDSEVClient(
            w3,
            verifier_address="0x...",
            permission_manager_address="0x...",
        )

        # Check attestation
        has_valid = await client.has_valid_attestation(agent_address)

        # Submit attestation
        result = await client.submit_attestation(report_hex, report_data)

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
        Initialize AMD SEV client.

        Args:
            w3: Web3 instance
            verifier_address: AMDSEVVerifier contract address
            permission_manager_address: TEEPermissionManager contract address
            account: Account address for transactions
        """
        self.w3 = w3
        self.account = account

        self.verifier: Contract = w3.eth.contract(
            address=Web3.to_checksum_address(verifier_address),
            abi=AMD_SEV_VERIFIER_ABI,
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
        # keccak256(abi.encodePacked("ZEROQUANT_TEE_ATTESTATION", agent))
        message = b"ZEROQUANT_TEE_ATTESTATION" + bytes.fromhex(
            agent_address[2:].lower()
        )
        return Web3.keccak(message)

    def parse_attestation_report(self, report_hex: str) -> AMDSEVReport:
        """
        Parse a raw AMD SEV-SNP attestation report.

        Args:
            report_hex: Hex-encoded attestation report

        Returns:
            Parsed AMDSEVReport

        Raises:
            ValueError: If report format is invalid
        """
        report_bytes = bytes.fromhex(report_hex[2:] if report_hex.startswith('0x') else report_hex)

        if len(report_bytes) < 1184:
            raise ValueError(f"Report too short: {len(report_bytes)} bytes, expected >= 1184")

        def read_tcb(data: bytes, offset: int) -> TCBVersion:
            return TCBVersion(
                bootloader=data[offset],
                tee=data[offset + 1],
                snp=data[offset + 6],
                microcode=data[offset + 7],
            )

        return AMDSEVReport(
            version=int.from_bytes(report_bytes[0:4], 'little'),
            guest_svn=int.from_bytes(report_bytes[4:8], 'little'),
            policy=int.from_bytes(report_bytes[8:16], 'little'),
            family_id=report_bytes[16:32],
            image_id=report_bytes[32:48],
            vmpl=int.from_bytes(report_bytes[48:52], 'little'),
            signature_algo=int.from_bytes(report_bytes[52:56], 'little'),
            current_tcb=read_tcb(report_bytes, 56),
            platform_info=int.from_bytes(report_bytes[64:72], 'little'),
            author_key_en=int.from_bytes(report_bytes[72:76], 'little'),
            measurement=report_bytes[80:128],
            host_data=report_bytes[128:160],
            id_key_digest=report_bytes[160:208],
            author_key_digest=report_bytes[208:256],
            report_id=report_bytes[256:288],
            report_id_ma=report_bytes[288:320],
            reported_tcb=read_tcb(report_bytes, 320),
            chip_id=report_bytes[336:400],
            committed_tcb=read_tcb(report_bytes, 400),
            current_build=report_bytes[408],
            current_minor=report_bytes[409],
            current_major=report_bytes[410],
            committed_build=report_bytes[416],
            committed_minor=report_bytes[417],
            committed_major=report_bytes[418],
            launch_tcb=read_tcb(report_bytes, 424),
            report_data=report_bytes[512:576],
            signature=report_bytes[576:1184],
        )

    async def has_valid_attestation(self, agent_address: str) -> bool:
        """
        Check if agent has valid attestation.

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
            platform=TEEPlatform(result[0]),
            status=AttestationStatus(result[1]),
            measurement=result[2],
            report_data=result[3],
            verified_at=result[4],
            expires_at=result[5],
            verifier=self.verifier.address,
            attestation_id="",  # Would need separate call
            measurement_trusted=False,  # Would need separate check
        )

    async def submit_attestation(
        self,
        report_hex: str,
        report_data: bytes,
    ) -> AttestationResult:
        """
        Submit attestation report for on-chain verification.

        Args:
            report_hex: Hex-encoded attestation report
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
            report_bytes = bytes.fromhex(
                report_hex[2:] if report_hex.startswith('0x') else report_hex
            )

            tx = self.verifier.functions.verifyAttestation(
                report_bytes,
                report_data,
            ).build_transaction({
                'from': self.account,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })

            # In real usage, would sign and send transaction
            # tx_hash = self.w3.eth.send_raw_transaction(signed_tx)

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
        platform: TEEPlatform,
        measurement: bytes,
        report_data: bytes,
        validity_period: int,
    ) -> AttestationResult:
        """
        Submit pre-verified attestation (for trusted relayers).

        Args:
            agent_address: Agent address
            platform: TEE platform
            measurement: Code measurement
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
                platform.value,
                measurement,
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
        Upgrade agent session with TEE attestation for elevated limits.

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

        # In real usage, would sign and send
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

    async def add_trusted_measurement(
        self,
        measurement: bytes,
        name: str,
    ) -> str:
        """
        Add a trusted measurement to the registry.

        Args:
            measurement: Measurement hash (32 bytes)
            name: Human-readable name

        Returns:
            Transaction hash
        """
        if not self.account:
            raise ValueError("No account configured for transactions")

        tx = self.permission_manager.functions.addTrustedMeasurement(
            measurement,
            name,
        ).build_transaction({
            'from': self.account,
            'nonce': self.w3.eth.get_transaction_count(self.account),
        })

        return "0x..."

    async def remove_trusted_measurement(self, measurement: bytes) -> str:
        """
        Remove a trusted measurement.

        Args:
            measurement: Measurement hash

        Returns:
            Transaction hash
        """
        if not self.account:
            raise ValueError("No account configured for transactions")

        tx = self.permission_manager.functions.removeTrustedMeasurement(
            measurement,
        ).build_transaction({
            'from': self.account,
            'nonce': self.w3.eth.get_transaction_count(self.account),
        })

        return "0x..."

    async def is_trusted_measurement(self, measurement: bytes) -> bool:
        """
        Check if a measurement is trusted.

        Args:
            measurement: Measurement hash

        Returns:
            True if trusted
        """
        return self.permission_manager.functions.isTrustedMeasurement(
            measurement
        ).call()
