"""
Tests for ZeroQuant TEE Integration Module
"""

import pytest
from zeroquant.tee import (
    TEEPlatform,
    AttestationStatus,
    TCBVersion,
    AMDSEVReport,
    TEEAttestation,
    TrustedMeasurement,
    EffectiveLimits,
    AttestationResult,
    AMDSEVClient,
    # Intel TDX
    IntelTDXClient,
    TDXQuote,
    TDReport,
    TDInfo,
    TDXTCBInfo,
)


class TestTEEModels:
    """Test TEE model classes."""

    def test_tee_platform_enum(self):
        """Test TEEPlatform enum values."""
        assert TEEPlatform.NONE == 0
        assert TEEPlatform.AMD_SEV_SNP == 1
        assert TEEPlatform.INTEL_TDX == 2
        assert TEEPlatform.ARM_TRUSTZONE == 3

    def test_attestation_status_enum(self):
        """Test AttestationStatus enum values."""
        assert AttestationStatus.NONE == 0
        assert AttestationStatus.PENDING == 1
        assert AttestationStatus.VERIFIED == 2
        assert AttestationStatus.EXPIRED == 3
        assert AttestationStatus.REVOKED == 4
        assert AttestationStatus.FAILED == 5

    def test_tcb_version_creation(self):
        """Test TCBVersion creation."""
        tcb = TCBVersion(
            bootloader=1,
            tee=2,
            snp=3,
            microcode=4,
        )

        assert tcb.bootloader == 1
        assert tcb.tee == 2
        assert tcb.snp == 3
        assert tcb.microcode == 4

    def test_tee_attestation_creation(self):
        """Test TEEAttestation creation."""
        attestation = TEEAttestation(
            agent="0x1234567890123456789012345678901234567890",
            platform=TEEPlatform.AMD_SEV_SNP,
            status=AttestationStatus.VERIFIED,
            measurement=bytes(32),
            report_data=bytes(32),
            verified_at=1700000000,
            expires_at=1700086400,
            verifier="0xabcdef1234567890123456789012345678901234",
            attestation_id="att_12345",
            measurement_trusted=True,
        )

        assert attestation.platform == TEEPlatform.AMD_SEV_SNP
        assert attestation.status == AttestationStatus.VERIFIED
        assert attestation.measurement_trusted is True

    def test_effective_limits_creation(self):
        """Test EffectiveLimits creation."""
        limits = EffectiveLimits(
            daily_limit=30_000_000_000,  # $30,000
            per_tx_limit=3_000_000_000,   # $3,000
            daily_spent=5_000_000_000,    # $5,000
            using_tee_limits=True,
            tee_expires_at=1700086400,
            session_expires_at=1700172800,
        )

        assert limits.daily_limit == 30_000_000_000
        assert limits.using_tee_limits is True
        assert limits.tee_expires_at == 1700086400

    def test_effective_limits_without_tee(self):
        """Test EffectiveLimits without TEE."""
        limits = EffectiveLimits(
            daily_limit=10_000_000_000,  # $10,000
            per_tx_limit=1_000_000_000,   # $1,000
            daily_spent=0,
            using_tee_limits=False,
            tee_expires_at=None,
            session_expires_at=1700172800,
        )

        assert limits.using_tee_limits is False
        assert limits.tee_expires_at is None

    def test_attestation_result_success(self):
        """Test AttestationResult for success case."""
        result = AttestationResult(
            success=True,
            attestation_id="att_12345",
            tx_hash="0xabc123...",
        )

        assert result.success is True
        assert result.attestation_id == "att_12345"
        assert result.error is None

    def test_attestation_result_failure(self):
        """Test AttestationResult for failure case."""
        result = AttestationResult(
            success=False,
            error="Invalid attestation report",
        )

        assert result.success is False
        assert result.attestation_id is None
        assert result.error == "Invalid attestation report"

    def test_trusted_measurement_creation(self):
        """Test TrustedMeasurement creation."""
        measurement = TrustedMeasurement(
            measurement=bytes(32),
            name="Production Agent v1.0.0",
            added_at=1700000000,
            added_by="0x1234567890123456789012345678901234567890",
            active=True,
        )

        assert measurement.name == "Production Agent v1.0.0"
        assert measurement.active is True


class TestAMDSEVClient:
    """Test AMD SEV Client functionality (mock tests)."""

    def test_create_report_data(self):
        """Test report data creation."""
        # Note: This would need a mock Web3 instance in real tests
        # For now, we test the algorithm directly
        from web3 import Web3

        agent_address = "0x1234567890123456789012345678901234567890"
        message = b"ZEROQUANT_TEE_ATTESTATION" + bytes.fromhex(agent_address[2:].lower())
        report_data = Web3.keccak(message)

        assert len(report_data) == 32
        assert isinstance(report_data, bytes)

    def test_parse_attestation_report_too_short(self):
        """Test that short reports raise an error."""
        from unittest.mock import MagicMock

        # Create mock Web3 and contract
        mock_w3 = MagicMock()
        mock_w3.eth.contract.return_value = MagicMock()

        client = AMDSEVClient(
            w3=mock_w3,
            verifier_address="0x1234567890123456789012345678901234567890",
            permission_manager_address="0xabcdef1234567890123456789012345678901234",
        )

        with pytest.raises(ValueError, match="Report too short"):
            client.parse_attestation_report("0x" + "00" * 100)

    def test_parse_attestation_report_valid(self):
        """Test parsing a valid (mock) attestation report."""
        from unittest.mock import MagicMock

        mock_w3 = MagicMock()
        mock_w3.eth.contract.return_value = MagicMock()

        client = AMDSEVClient(
            w3=mock_w3,
            verifier_address="0x1234567890123456789012345678901234567890",
            permission_manager_address="0xabcdef1234567890123456789012345678901234",
        )

        # Create a mock report of sufficient length
        mock_report = "0x" + "00" * 1184

        report = client.parse_attestation_report(mock_report)

        assert report.version == 0
        assert isinstance(report.current_tcb, TCBVersion)
        assert len(report.measurement) == 48
        assert len(report.report_data) == 64


class TestTEEIntegration:
    """Integration-style tests for TEE functionality."""

    def test_attestation_workflow(self):
        """Test typical attestation workflow."""
        # Create attestation
        attestation = TEEAttestation(
            agent="0x1234567890123456789012345678901234567890",
            platform=TEEPlatform.AMD_SEV_SNP,
            status=AttestationStatus.PENDING,
            measurement=bytes(32),
            report_data=bytes(32),
            verified_at=0,
            expires_at=0,
            verifier="0xabcdef1234567890123456789012345678901234",
            attestation_id="",
            measurement_trusted=False,
        )

        assert attestation.status == AttestationStatus.PENDING

        # Simulate verification
        attestation.status = AttestationStatus.VERIFIED
        attestation.verified_at = 1700000000
        attestation.expires_at = 1700086400
        attestation.measurement_trusted = True

        assert attestation.status == AttestationStatus.VERIFIED
        assert attestation.measurement_trusted is True

    def test_limits_upgrade_with_tee(self):
        """Test limits upgrade with TEE attestation."""
        # Standard limits
        standard_limits = EffectiveLimits(
            daily_limit=10_000_000_000,
            per_tx_limit=1_000_000_000,
            daily_spent=0,
            using_tee_limits=False,
            session_expires_at=1700172800,
        )

        # TEE-elevated limits (3x)
        tee_limits = EffectiveLimits(
            daily_limit=30_000_000_000,
            per_tx_limit=3_000_000_000,
            daily_spent=0,
            using_tee_limits=True,
            tee_expires_at=1700086400,
            session_expires_at=1700259200,
        )

        assert tee_limits.daily_limit == standard_limits.daily_limit * 3
        assert tee_limits.per_tx_limit == standard_limits.per_tx_limit * 3
        assert tee_limits.using_tee_limits is True

    def test_tcb_version_comparison(self):
        """Test TCB version comparison."""
        min_tcb = TCBVersion(bootloader=1, tee=2, snp=3, microcode=4)
        current_tcb = TCBVersion(bootloader=2, tee=3, snp=4, microcode=5)

        # Current TCB should meet minimum requirements
        assert current_tcb.bootloader >= min_tcb.bootloader
        assert current_tcb.tee >= min_tcb.tee
        assert current_tcb.snp >= min_tcb.snp
        assert current_tcb.microcode >= min_tcb.microcode

    def test_attestation_expiry_check(self):
        """Test attestation expiry checking."""
        import time

        current_time = int(time.time())

        # Valid attestation
        valid_attestation = TEEAttestation(
            agent="0x1234567890123456789012345678901234567890",
            platform=TEEPlatform.AMD_SEV_SNP,
            status=AttestationStatus.VERIFIED,
            measurement=bytes(32),
            report_data=bytes(32),
            verified_at=current_time - 3600,  # 1 hour ago
            expires_at=current_time + 86400,  # 24 hours from now
            verifier="0xabcdef1234567890123456789012345678901234",
            attestation_id="att_valid",
            measurement_trusted=True,
        )

        # Expired attestation
        expired_attestation = TEEAttestation(
            agent="0x1234567890123456789012345678901234567890",
            platform=TEEPlatform.AMD_SEV_SNP,
            status=AttestationStatus.EXPIRED,
            measurement=bytes(32),
            report_data=bytes(32),
            verified_at=current_time - 172800,  # 2 days ago
            expires_at=current_time - 86400,    # Expired 1 day ago
            verifier="0xabcdef1234567890123456789012345678901234",
            attestation_id="att_expired",
            measurement_trusted=True,
        )

        assert valid_attestation.expires_at > current_time
        assert expired_attestation.expires_at < current_time


class TestIntelTDXModels:
    """Test Intel TDX model classes."""

    def test_tdx_tcb_info_creation(self):
        """Test TDXTCBInfo creation."""
        tcb = TDXTCBInfo(
            sgx_tcb_comp_svn=[1, 2, 3, 4, 5, 6, 7, 8],
            pce_svn=10,
            tdx_tcb_comp_svn=[1, 2, 3, 4],
        )

        assert len(tcb.sgx_tcb_comp_svn) == 8
        assert tcb.pce_svn == 10
        assert len(tcb.tdx_tcb_comp_svn) == 4

    def test_td_info_creation(self):
        """Test TDInfo creation."""
        td_info = TDInfo(
            attributes=bytes(8),
            xfam=bytes(8),
            mr_td=bytes(48),
            mr_config_id=bytes(48),
            mr_owner=bytes(48),
            mr_owner_config=bytes(48),
            rt_mr=[bytes(48), bytes(48), bytes(48), bytes(48)],
        )

        assert len(td_info.mr_td) == 48
        assert len(td_info.rt_mr) == 4
        assert len(td_info.attributes) == 8

    def test_td_report_creation(self):
        """Test TDReport creation."""
        td_info = TDInfo(
            attributes=bytes(8),
            xfam=bytes(8),
            mr_td=bytes(48),
            mr_config_id=bytes(48),
            mr_owner=bytes(48),
            mr_owner_config=bytes(48),
            rt_mr=[bytes(48), bytes(48), bytes(48), bytes(48)],
        )

        report = TDReport(
            report_type=bytes(4),
            cpu_svn=bytes(16),
            tee_tcb_info_hash=bytes(48),
            tee_info_hash=bytes(48),
            report_data=bytes(64),
            td_info=td_info,
        )

        assert len(report.report_data) == 64
        assert len(report.cpu_svn) == 16
        assert report.td_info == td_info

    def test_tdx_quote_creation(self):
        """Test TDXQuote creation."""
        td_info = TDInfo(
            attributes=bytes(8),
            xfam=bytes(8),
            mr_td=bytes(48),
            mr_config_id=bytes(48),
            mr_owner=bytes(48),
            mr_owner_config=bytes(48),
            rt_mr=[bytes(48), bytes(48), bytes(48), bytes(48)],
        )

        report = TDReport(
            report_type=bytes(4),
            cpu_svn=bytes(16),
            tee_tcb_info_hash=bytes(48),
            tee_info_hash=bytes(48),
            report_data=bytes(64),
            td_info=td_info,
        )

        quote = TDXQuote(
            version=4,
            attestation_key_type=2,
            tee_type=0x81,
            qe_svn=5,
            pce_svn=12,
            qe_vendor_id=bytes(16),
            user_data=bytes(20),
            td_report=report,
            signature=bytes(64),
        )

        assert quote.version == 4
        assert quote.tee_type == 0x81
        assert quote.td_report == report

    def test_tdx_platform_enum(self):
        """Test TDX platform is correctly defined."""
        assert TEEPlatform.INTEL_TDX == 2


class TestIntelTDXClient:
    """Test Intel TDX Client functionality (mock tests)."""

    def test_client_initialization(self):
        """Test Intel TDX client initialization."""
        from unittest.mock import MagicMock

        mock_w3 = MagicMock()
        mock_w3.eth.contract.return_value = MagicMock()

        client = IntelTDXClient(
            w3=mock_w3,
            verifier_address="0x1234567890123456789012345678901234567890",
            permission_manager_address="0xabcdef1234567890123456789012345678901234",
        )

        assert client is not None

    def test_is_tdx_quote_valid_version(self):
        """Test TDX quote TEE type detection."""
        from unittest.mock import MagicMock

        mock_w3 = MagicMock()
        mock_w3.eth.contract.return_value = MagicMock()

        client = IntelTDXClient(
            w3=mock_w3,
            verifier_address="0x1234567890123456789012345678901234567890",
            permission_manager_address="0xabcdef1234567890123456789012345678901234",
        )

        # Valid TDX quote has version 4 and tee_type 0x81 at offset 0x04
        # Build quote: version (2 bytes) + attestation_key_type (2 bytes) + tee_type (4 bytes) + rest
        quote_bytes = b'\x04\x00'  # version 4
        quote_bytes += b'\x02\x00'  # attestation_key_type
        quote_bytes += b'\x81\x00\x00\x00'  # tee_type 0x81 (TDX)
        quote_bytes += b'\x00' * 1000  # padding to meet minimum length
        valid_quote = "0x" + quote_bytes.hex()
        assert client.is_tdx_quote(valid_quote) is True

    def test_is_tdx_quote_invalid_version(self):
        """Test TDX quote version detection for invalid quotes."""
        from unittest.mock import MagicMock

        mock_w3 = MagicMock()
        mock_w3.eth.contract.return_value = MagicMock()

        client = IntelTDXClient(
            w3=mock_w3,
            verifier_address="0x1234567890123456789012345678901234567890",
            permission_manager_address="0xabcdef1234567890123456789012345678901234",
        )

        # Invalid version (3)
        invalid_quote = "0x0300" + "00" * 1000
        assert client.is_tdx_quote(invalid_quote) is False

    def test_parse_quote_too_short(self):
        """Test that short quotes raise an error."""
        from unittest.mock import MagicMock

        mock_w3 = MagicMock()
        mock_w3.eth.contract.return_value = MagicMock()

        client = IntelTDXClient(
            w3=mock_w3,
            verifier_address="0x1234567890123456789012345678901234567890",
            permission_manager_address="0xabcdef1234567890123456789012345678901234",
        )

        with pytest.raises(ValueError, match="Quote too short"):
            client.parse_quote("0x" + "00" * 50)

    def test_parse_quote_valid(self):
        """Test parsing a valid (mock) TDX quote."""
        from unittest.mock import MagicMock

        mock_w3 = MagicMock()
        mock_w3.eth.contract.return_value = MagicMock()

        client = IntelTDXClient(
            w3=mock_w3,
            verifier_address="0x1234567890123456789012345678901234567890",
            permission_manager_address="0xabcdef1234567890123456789012345678901234",
        )

        # Create a mock quote of sufficient length (at least 700 bytes)
        mock_quote = "0x" + "00" * 800

        quote = client.parse_quote(mock_quote)

        assert quote.version == 0
        assert quote.td_report is not None
        assert len(quote.td_report.report_data) == 64

    def test_extract_mrtd(self):
        """Test MRTD extraction from quote.

        Note: extract_mr_td returns only first 32 bytes (for EVM compatibility).
        """
        from unittest.mock import MagicMock

        mock_w3 = MagicMock()
        mock_w3.eth.contract.return_value = MagicMock()

        client = IntelTDXClient(
            w3=mock_w3,
            verifier_address="0x1234567890123456789012345678901234567890",
            permission_manager_address="0xabcdef1234567890123456789012345678901234",
        )

        # Create mock quote with known MRTD value
        # MRTD is at TD_INFO_MRTD offset (0xB0 = 176) from TD_REPORT offset (0x44 = 68)
        # So MRTD starts at 68 + 176 = 244 bytes
        mock_quote = "0x" + "00" * 244 + "ab" * 48 + "00" * 500

        mr_td = client.extract_mr_td(mock_quote)

        # Method returns first 32 bytes for EVM compatibility
        assert len(mr_td) == 32
        assert mr_td == bytes.fromhex("ab" * 32)

    def test_create_report_data(self):
        """Test report data creation for TDX."""
        from web3 import Web3

        agent_address = "0x1234567890123456789012345678901234567890"
        message = b"ZEROQUANT_TDX_ATTESTATION" + bytes.fromhex(agent_address[2:].lower())
        report_data = Web3.keccak(message)

        assert len(report_data) == 32
        assert isinstance(report_data, bytes)


class TestTDXIntegration:
    """Integration-style tests for Intel TDX functionality."""

    def test_tdx_attestation_workflow(self):
        """Test typical TDX attestation workflow."""
        # Create attestation with Intel TDX platform
        attestation = TEEAttestation(
            agent="0x1234567890123456789012345678901234567890",
            platform=TEEPlatform.INTEL_TDX,
            status=AttestationStatus.PENDING,
            measurement=bytes(48),  # MRTD is 48 bytes
            report_data=bytes(64),  # TDX report data is 64 bytes
            verified_at=0,
            expires_at=0,
            verifier="0xabcdef1234567890123456789012345678901234",
            attestation_id="",
            measurement_trusted=False,
        )

        assert attestation.platform == TEEPlatform.INTEL_TDX
        assert attestation.status == AttestationStatus.PENDING

        # Simulate verification
        attestation.status = AttestationStatus.VERIFIED
        attestation.verified_at = 1700000000
        attestation.expires_at = 1700086400
        attestation.measurement_trusted = True

        assert attestation.status == AttestationStatus.VERIFIED
        assert attestation.measurement_trusted is True

    def test_tdx_limits_upgrade(self):
        """Test limits upgrade with TDX attestation."""
        # Standard limits
        standard_limits = EffectiveLimits(
            daily_limit=10_000_000_000,
            per_tx_limit=1_000_000_000,
            daily_spent=0,
            using_tee_limits=False,
            session_expires_at=1700172800,
        )

        # TDX-elevated limits (3x)
        tdx_limits = EffectiveLimits(
            daily_limit=30_000_000_000,
            per_tx_limit=3_000_000_000,
            daily_spent=0,
            using_tee_limits=True,
            tee_expires_at=1700086400,
            session_expires_at=1700259200,
        )

        assert tdx_limits.daily_limit == standard_limits.daily_limit * 3
        assert tdx_limits.per_tx_limit == standard_limits.per_tx_limit * 3
        assert tdx_limits.using_tee_limits is True

    def test_multi_platform_support(self):
        """Test that both AMD SEV and Intel TDX are supported."""
        amd_attestation = TEEAttestation(
            agent="0x1111111111111111111111111111111111111111",
            platform=TEEPlatform.AMD_SEV_SNP,
            status=AttestationStatus.VERIFIED,
            measurement=bytes(48),
            report_data=bytes(64),
            verified_at=1700000000,
            expires_at=1700086400,
            verifier="0xabcdef1234567890123456789012345678901234",
            attestation_id="att_amd_1",
            measurement_trusted=True,
        )

        tdx_attestation = TEEAttestation(
            agent="0x2222222222222222222222222222222222222222",
            platform=TEEPlatform.INTEL_TDX,
            status=AttestationStatus.VERIFIED,
            measurement=bytes(48),
            report_data=bytes(64),
            verified_at=1700000000,
            expires_at=1700086400,
            verifier="0xabcdef1234567890123456789012345678901234",
            attestation_id="att_tdx_1",
            measurement_trusted=True,
        )

        assert amd_attestation.platform == TEEPlatform.AMD_SEV_SNP
        assert tdx_attestation.platform == TEEPlatform.INTEL_TDX
        assert amd_attestation.status == tdx_attestation.status
