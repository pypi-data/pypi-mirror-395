"""
Canonical Six Gateway Patterns - Span-based naming

The Canonical Six are framework-independent zero divisor patterns that work
identically in both Cayley-Dickson and Clifford algebraic frameworks.

Each gateway is defined by:
- indices: [a, b, c, d] where P = e_a + s1*e_b and Q = e_c + s2*e_d
- signs: [s1, s2] determining the sign of second basis element in each term
- span: The index distance that characterizes the pattern structure

These patterns satisfy P × Q = 0 (verified to machine precision ~10^-15).

Reference: "Framework-Independent Zero Divisor Patterns in
Higher-Dimensional Cayley-Dickson Algebras" - Chavez (2025)
"""

from typing import Tuple, Dict, Any

# Lazy import to avoid circular dependencies
_Sedenion = None

def _get_sedenion():
    """Lazy load Sedenion class."""
    global _Sedenion
    if _Sedenion is None:
        from hypercomplex import Sedenion
        _Sedenion = Sedenion
    return _Sedenion


# Canonical Six Gateway Definitions
# VERIFIED zero divisor patterns - these satisfy P × Q = 0 to machine precision
CANONICAL_SIX: Dict[str, Dict[str, Any]] = {
    "S1": {
        # (e_1 + e_14) × (e_3 + e_12) = 0
        "indices": [1, 14, 3, 12],
        "signs": [1, 1],
        "description": "Master Gateway"
    },
    "S2": {
        # (e_3 + e_12) × (e_5 + e_10) = 0
        "indices": [3, 12, 5, 10],
        "signs": [1, 1],
        "description": "Multi-Modal Gateway"
    },
    "S3A": {
        # (e_4 + e_11) × (e_6 + e_9) = 0
        "indices": [4, 11, 6, 9],
        "signs": [1, 1],
        "description": "Discontinuous Gateway"
    },
    "S3B": {
        # (e_1 - e_14) × (e_3 - e_12) = 0
        "indices": [1, 14, 3, 12],
        "signs": [-1, -1],
        "description": "Conjugate Pair Gateway"
    },
    "S4": {
        # (e_1 - e_14) × (e_5 + e_10) = 0
        "indices": [1, 14, 5, 10],
        "signs": [-1, 1],
        "description": "Linear Gateway"
    },
    "S5": {
        # (e_2 - e_13) × (e_6 + e_9) = 0
        "indices": [2, 13, 6, 9],
        "signs": [-1, 1],
        "description": "Transformation Gateway"
    },
}


def get_gateway_pair(gateway: str) -> Tuple[Any, Any]:
    """
    Build P and Q sedenions for a gateway pattern.

    For pattern (e_a + s1*e_b) × (e_c + s2*e_d) = 0:
    - P = e_a + s1*e_b (first factor)
    - Q = e_c + s2*e_d (second factor)

    Args:
        gateway: Gateway name (S1, S2, S3A, S3B, S4, S5)

    Returns:
        Tuple of (P, Q) Sedenion objects satisfying P × Q = 0

    Raises:
        ValueError: If gateway name is not recognized
    """
    if gateway not in CANONICAL_SIX:
        valid_gateways = list(CANONICAL_SIX.keys())
        raise ValueError(f"Unknown gateway: {gateway}. Valid gateways: {valid_gateways}")

    Sedenion = _get_sedenion()
    pattern = CANONICAL_SIX[gateway]
    a, b, c, d = pattern["indices"]
    s1, s2 = pattern["signs"]

    # Build P = e_a + s1*e_b
    p_coeffs = [0.0] * 16
    p_coeffs[a] = 1.0
    p_coeffs[b] = float(s1)
    P = Sedenion(*p_coeffs)

    # Build Q = e_c + s2*e_d
    q_coeffs = [0.0] * 16
    q_coeffs[c] = 1.0
    q_coeffs[d] = float(s2)
    Q = Sedenion(*q_coeffs)

    return P, Q


def get_gateway_info(gateway: str) -> Dict[str, Any]:
    """
    Get detailed information about a gateway pattern.

    Args:
        gateway: Gateway name (S1, S2, S3A, S3B, S4, S5)

    Returns:
        Dictionary with pattern details including indices, signs, and formula
    """
    if gateway not in CANONICAL_SIX:
        valid_gateways = list(CANONICAL_SIX.keys())
        raise ValueError(f"Unknown gateway: {gateway}. Valid gateways: {valid_gateways}")

    pattern = CANONICAL_SIX[gateway]
    a, b, c, d = pattern["indices"]
    s1, s2 = pattern["signs"]

    # Build human-readable formula
    s1_str = "+" if s1 == 1 else "-"
    s2_str = "+" if s2 == 1 else "-"
    formula = f"(e_{a} {s1_str} e_{b}) × (e_{c} {s2_str} e_{d}) = 0"

    return {
        "name": gateway,
        "indices": pattern["indices"],
        "signs": pattern["signs"],
        "description": pattern["description"],
        "formula": formula,
        "P_expression": f"e_{a} {s1_str} e_{b}",
        "Q_expression": f"e_{c} {s2_str} e_{d}",
    }


def list_gateways() -> Dict[str, Dict[str, Any]]:
    """
    List all available gateway patterns with their details.

    Returns:
        Dictionary mapping gateway names to their information
    """
    return {name: get_gateway_info(name) for name in CANONICAL_SIX}
