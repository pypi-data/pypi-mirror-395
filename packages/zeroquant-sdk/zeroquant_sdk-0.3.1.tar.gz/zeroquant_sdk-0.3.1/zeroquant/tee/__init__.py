"""
ZeroQuant TEE Integration Module

Provides TEE attestation support for elevated agent permissions.

Supported Platforms:
- AMD SEV-SNP (Secure Encrypted Virtualization - Secure Nested Paging)
- Intel TDX (Trust Domain Extensions)
"""

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
from .client import AMDSEVClient
from .intel_tdx import (
    IntelTDXClient,
    TDXQuote,
    TDReport,
    TDInfo,
    TDXTCBInfo,
)

__all__ = [
    # Models
    "TEEPlatform",
    "AttestationStatus",
    "TCBVersion",
    "AMDSEVReport",
    "TEEAttestation",
    "TrustedMeasurement",
    "EffectiveLimits",
    "AttestationResult",
    # AMD SEV Client
    "AMDSEVClient",
    # Intel TDX Client
    "IntelTDXClient",
    "TDXQuote",
    "TDReport",
    "TDInfo",
    "TDXTCBInfo",
]
