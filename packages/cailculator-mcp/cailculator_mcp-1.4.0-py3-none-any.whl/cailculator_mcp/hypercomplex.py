"""
Hypercomplex Number Systems - Wrapper for real hypercomplex library
Re-exports from the hypercomplex library (v0.3.4) with MCP-specific utilities
"""

import numpy as np
from typing import Tuple, List
import logging

# Import from real hypercomplex library
from hypercomplex import Sedenion, Pathion, Chingon, CD128, CD256

logger = logging.getLogger(__name__)

# Re-export classes
__all__ = ['Sedenion', 'Pathion', 'Chingon', 'CD128', 'CD256', 'create_hypercomplex', 'find_zero_divisors']


def create_hypercomplex(dimension: int, coefficients: List[float]):
    """
    Factory function to create hypercomplex number of specified dimension.

    Args:
        dimension: Must be 16, 32, 64, 128, or 256
        coefficients: List of real coefficients

    Returns:
        Appropriate hypercomplex number instance from real library

    Supported Dimensions:
        - 16D: Sedenions (S)
        - 32D: Pathions (P)
        - 64D: Chingons (X)
        - 128D: CD128 (next Cayley-Dickson level)
        - 256D: CD256 (next Cayley-Dickson level)

    Note: 512D and beyond require custom implementation (not in hypercomplex library)
    """
    if dimension == 16:
        return Sedenion(*coefficients)
    elif dimension == 32:
        return Pathion(*coefficients)
    elif dimension == 64:
        return Chingon(*coefficients)
    elif dimension == 128:
        return CD128(*coefficients)
    elif dimension == 256:
        return CD256(*coefficients)
    else:
        raise ValueError(f"Unsupported dimension {dimension}. Supported: 16, 32, 64, 128, 256 (512+ not yet available).")


def find_zero_divisors(dimension: int, num_samples: int = 1000) -> List[Tuple]:
    """
    Search for pairs of zero divisors in specified dimension.

    Uses known Canonical Six patterns for sedenions, random search for higher dimensions.

    Args:
        dimension: Algebra dimension (16, 32, 64)
        num_samples: Number of random pairs to test

    Returns:
        List of (x, y) pairs where xy ≈ 0 but x, y != 0
    """
    if dimension < 16:
        logger.info(f"No zero divisors exist in dimension {dimension}")
        return []

    zero_divisor_pairs = []

    # For sedenions (16D), use known Canonical Six patterns
    if dimension == 16:
        # Canonical Six pattern 1: (e_1 + e_10) × (e_4 - e_15) = 0
        p1_coeffs = [0.0] * 16
        p1_coeffs[1] = 1.0
        p1_coeffs[10] = 1.0

        q1_coeffs = [0.0] * 16
        q1_coeffs[4] = 1.0
        q1_coeffs[15] = -1.0

        p1 = Sedenion(*p1_coeffs)
        q1 = Sedenion(*q1_coeffs)

        zero_divisor_pairs.append((p1, q1))

        # Add a few more known patterns
        # Pattern 2: (e_1 + e_10) × (e_5 + e_14) = 0
        p2_coeffs = [0.0] * 16
        p2_coeffs[1] = 1.0
        p2_coeffs[10] = 1.0

        q2_coeffs = [0.0] * 16
        q2_coeffs[5] = 1.0
        q2_coeffs[14] = 1.0

        p2 = Sedenion(*p2_coeffs)
        q2 = Sedenion(*q2_coeffs)

        zero_divisor_pairs.append((p2, q2))

        return zero_divisor_pairs

    # For pathions (32D), use extended Canonical Six
    elif dimension == 32:
        # Pattern 1 in 32D: (e_1 + e_14) × (e_4 - e_11) = 0
        p1_coeffs = [0.0] * 32
        p1_coeffs[1] = 1.0
        p1_coeffs[14] = 1.0

        q1_coeffs = [0.0] * 32
        q1_coeffs[4] = 1.0
        q1_coeffs[11] = -1.0

        p1 = Pathion(*p1_coeffs)
        q1 = Pathion(*q1_coeffs)

        zero_divisor_pairs.append((p1, q1))

        return zero_divisor_pairs

    # For higher dimensions, use random search (fallback)
    else:
        for _ in range(min(num_samples, 100)):
            coeffs1 = np.zeros(dimension)
            coeffs2 = np.zeros(dimension)

            # Sparse random elements
            num_nonzero = min(4, dimension // 8)
            indices1 = np.random.choice(dimension, num_nonzero, replace=False)
            indices2 = np.random.choice(dimension, num_nonzero, replace=False)

            coeffs1[indices1] = np.random.randn(num_nonzero)
            coeffs2[indices2] = np.random.randn(num_nonzero)

            try:
                x = create_hypercomplex(dimension, coeffs1.tolist())
                y = create_hypercomplex(dimension, coeffs2.tolist())

                product = x * y

                if abs(product) < 1e-8 and abs(x) > 1e-2 and abs(y) > 1e-2:
                    zero_divisor_pairs.append((x, y))

                    if len(zero_divisor_pairs) >= 5:
                        break
            except:
                continue

        return zero_divisor_pairs


if __name__ == "__main__":
    print("="*70)
    print("HYPERCOMPLEX LIBRARY WRAPPER - Using real hypercomplex v0.3.4")
    print("="*70)
    print()

    # Test sedenion zero divisor
    print("SEDENION ZERO DIVISOR TEST")
    print("-" * 70)
    pairs = find_zero_divisors(16, num_samples=10)
    if pairs:
        p, q = pairs[0]
        product = p * q
        print(f"P = {p}")
        print(f"Q = {q}")
        print(f"|P| = {abs(p):.6f}")
        print(f"|Q| = {abs(q):.6f}")
        print(f"P × Q = {product}")
        print(f"|P × Q| = {abs(product):.2e}")
        print(f"Is zero divisor: {abs(product) < 1e-8}")
    print()

    # Test pathion zero divisor
    print("PATHION ZERO DIVISOR TEST")
    print("-" * 70)
    pairs32 = find_zero_divisors(32, num_samples=10)
    if pairs32:
        p, q = pairs32[0]
        product = p * q
        print(f"P = {p}")
        print(f"Q = {q}")
        print(f"|P| = {abs(p):.6f}")
        print(f"|Q| = {abs(q):.6f}")
        print(f"P × Q = {product}")
        print(f"|P × Q| = {abs(product):.2e}")
        print(f"Is zero divisor: {abs(product) < 1e-8}")
    print()
