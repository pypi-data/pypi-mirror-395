"""
ZDTP - Zero Divisor Transmission Protocol

Domain-agnostic implementation of the Zero Divisor Transmission Protocol
for transmitting data through verified mathematical gateways across
16D, 32D, and 64D hypercomplex spaces.

Reference: "Framework-Independent Zero Divisor Patterns in
Higher-Dimensional Cayley-Dickson Algebras" - Chavez (2025)
"""

from .gateways import CANONICAL_SIX, get_gateway_pair
from .protocol import ZDTPTransmission

__all__ = [
    "CANONICAL_SIX",
    "get_gateway_pair",
    "ZDTPTransmission",
]
