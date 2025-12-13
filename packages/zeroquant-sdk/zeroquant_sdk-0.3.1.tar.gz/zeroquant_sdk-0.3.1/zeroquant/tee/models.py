"""
TEE Models for ZeroQuant Python SDK
"""

from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel, Field


class TEEPlatform(IntEnum):
    """Supported TEE platforms."""
    NONE = 0
    AMD_SEV_SNP = 1
    INTEL_TDX = 2
    ARM_TRUSTZONE = 3


class AttestationStatus(IntEnum):
    """Attestation status codes."""
    NONE = 0
    PENDING = 1
    VERIFIED = 2
    EXPIRED = 3
    REVOKED = 4
    FAILED = 5


class TCBVersion(BaseModel):
    """Trusted Computing Base version components."""

    bootloader: int = Field(default=0, description="Bootloader version")
    tee: int = Field(default=0, description="TEE version")
    snp: int = Field(default=0, description="SNP firmware version")
    microcode: int = Field(default=0, description="Microcode version")


class AMDSEVReport(BaseModel):
    """Parsed AMD SEV-SNP attestation report."""

    version: int = Field(description="Report version")
    guest_svn: int = Field(description="Guest security version number")
    policy: int = Field(description="Guest policy flags")
    family_id: bytes = Field(description="Family ID (16 bytes)")
    image_id: bytes = Field(description="Image ID (16 bytes)")
    vmpl: int = Field(description="Virtual machine privilege level")
    signature_algo: int = Field(description="Signature algorithm")
    current_tcb: TCBVersion = Field(description="Current TCB version")
    platform_info: int = Field(description="Platform info flags")
    author_key_en: int = Field(description="Author key enabled flag")
    measurement: bytes = Field(description="Launch measurement (48 bytes)")
    host_data: bytes = Field(description="Host-provided data (32 bytes)")
    id_key_digest: bytes = Field(description="ID key digest (48 bytes)")
    author_key_digest: bytes = Field(description="Author key digest (48 bytes)")
    report_id: bytes = Field(description="Report ID (32 bytes)")
    report_id_ma: bytes = Field(description="Migration agent report ID (32 bytes)")
    reported_tcb: TCBVersion = Field(description="Reported TCB version")
    chip_id: bytes = Field(description="Chip ID (64 bytes)")
    committed_tcb: TCBVersion = Field(description="Committed TCB version")
    current_build: int = Field(description="Current build number")
    current_minor: int = Field(description="Current minor version")
    current_major: int = Field(description="Current major version")
    committed_build: int = Field(description="Committed build number")
    committed_minor: int = Field(description="Committed minor version")
    committed_major: int = Field(description="Committed major version")
    launch_tcb: TCBVersion = Field(description="Launch TCB version")
    report_data: bytes = Field(description="User-provided report data (64 bytes)")
    signature: bytes = Field(description="Report signature")

    class Config:
        arbitrary_types_allowed = True


class TEEAttestation(BaseModel):
    """On-chain TEE attestation record."""

    agent: str = Field(description="Agent address")
    platform: TEEPlatform = Field(description="TEE platform")
    status: AttestationStatus = Field(description="Attestation status")
    measurement: bytes = Field(description="Code measurement hash")
    report_data: bytes = Field(description="Report data binding")
    verified_at: int = Field(description="Verification timestamp")
    expires_at: int = Field(description="Expiration timestamp")
    verifier: str = Field(description="Verifier contract address")
    attestation_id: str = Field(description="Unique attestation ID")
    measurement_trusted: bool = Field(
        default=False,
        description="Whether measurement is in trusted registry"
    )

    class Config:
        arbitrary_types_allowed = True


class TrustedMeasurement(BaseModel):
    """Trusted code measurement entry."""

    measurement: bytes = Field(description="Measurement hash (32 bytes)")
    name: str = Field(description="Human-readable name")
    added_at: int = Field(description="Timestamp when added")
    added_by: str = Field(description="Address that added this measurement")
    active: bool = Field(default=True, description="Whether still trusted")

    class Config:
        arbitrary_types_allowed = True


class EffectiveLimits(BaseModel):
    """Effective agent limits (standard or TEE-elevated)."""

    daily_limit: int = Field(description="Daily spending limit (USD, 6 decimals)")
    per_tx_limit: int = Field(description="Per-transaction limit (USD, 6 decimals)")
    daily_spent: int = Field(default=0, description="Amount spent today")
    using_tee_limits: bool = Field(
        default=False,
        description="Whether TEE-elevated limits apply"
    )
    tee_expires_at: Optional[int] = Field(
        None,
        description="TEE attestation expiration timestamp"
    )
    session_expires_at: int = Field(description="Session expiration timestamp")


class AttestationResult(BaseModel):
    """Result of attestation submission."""

    success: bool = Field(description="Whether submission succeeded")
    attestation_id: Optional[str] = Field(None, description="Attestation ID if successful")
    tx_hash: Optional[str] = Field(None, description="Transaction hash")
    error: Optional[str] = Field(None, description="Error message if failed")
