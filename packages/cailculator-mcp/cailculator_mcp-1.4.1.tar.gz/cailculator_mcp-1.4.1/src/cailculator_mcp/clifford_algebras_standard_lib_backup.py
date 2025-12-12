"""
Clifford (Geometric) Algebras for Zero Divisor Analysis

This module provides Clifford algebra implementations of zero divisor patterns,
complementing the Cayley-Dickson algebra implementations in hypercomplex.py.

Key Insight: The Canonical Six zero divisor patterns can be expressed in BOTH:
1. Cayley-Dickson algebras (non-associative, via hypercomplex.py)
2. Clifford algebras (mostly associative, via this module)

This dual representation provides deeper mathematical insight into the structure
of zero divisors across different algebraic frameworks.
"""

import numpy as np
from clifford import Cl, MultiVector
from typing import Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)


class CliffordZeroDivisors:
    """
    Zero divisor patterns in Clifford (Geometric) Algebras.

    Clifford algebras Cl(p,q) are characterized by their signature (p,q):
    - p = number of basis vectors that square to +1
    - q = number of basis vectors that square to -1

    Zero divisors exist in certain Clifford algebras with specific signatures,
    particularly those with degenerate metrics (signature containing zeros).
    """

    def __init__(self, signature: Tuple[int, int, int] = None, dimension: int = None):
        """
        Initialize Clifford algebra with given signature OR dimension.

        Args:
            signature: (p, q, r) where:
                p = # of basis vectors with e_i^2 = +1
                q = # of basis vectors with e_i^2 = -1
                r = # of basis vectors with e_i^2 = 0 (degenerate/null)
            dimension: Multivector dimension (16, 32, 64, 128, 256)
                Automatically determines signature as Cl(log2(dim), 0, 0)

        Note: Provide either signature OR dimension, not both.
        """
        if dimension is not None:
            # Auto-determine signature from dimension
            # For dimension D, use Cl(n,0,0) where 2^n = D
            import math
            n = int(math.log2(dimension))
            if 2**n != dimension:
                raise ValueError(f"Dimension {dimension} must be power of 2")
            self.p, self.q, self.r = n, 0, 0
            logger.info(f"Auto-selected Cl({n},0,0) for {dimension}D multivector space")
        elif signature is not None:
            self.p, self.q, self.r = signature
        else:
            # Default to Cl(4,0,0) for 16D
            self.p, self.q, self.r = 4, 0, 0
            logger.info("Using default Cl(4,0,0) for 16D")

        self.signature_dimension = self.p + self.q + self.r
        self.multivector_dimension = 2 ** self.signature_dimension

        # Create the Clifford algebra
        # Note: Standard clifford library uses (p,q) signature
        # For degenerate metrics with r>0, we need special handling
        if self.r == 0:
            self.layout, self.blades = Cl(self.p, self.q, names='e')
        else:
            # Degenerate metric requires custom metric tensor
            metric = self._create_degenerate_metric()
            self.layout, self.blades = Cl(self.signature_dimension, metric=metric, names='e')

        logger.info(f"Initialized Cl({self.p},{self.q},{self.r}) - Signature dim: {self.signature_dimension}, Multivector dim: {self.multivector_dimension}")

    def _create_degenerate_metric(self) -> np.ndarray:
        """Create metric tensor for degenerate Clifford algebra"""
        n = self.signature_dimension
        metric = np.zeros((n, n))

        # Diagonal metric: +1 for first p, -1 for next q, 0 for last r
        for i in range(self.p):
            metric[i, i] = 1.0
        for i in range(self.p, self.p + self.q):
            metric[i, i] = -1.0
        # Last r diagonal elements remain 0 (degenerate)

        return metric

    def canonical_six_clifford(self, pattern_id: int = 1) -> Tuple[MultiVector, MultiVector]:
        """
        Create Canonical Six zero divisor pair in Clifford algebra.

        The Canonical Six patterns from Cayley-Dickson sedenions can be
        mapped to specific Clifford algebra elements. This provides an
        alternative representation with different multiplication rules.

        Args:
            pattern_id: 1-6 for the six canonical patterns

        Returns:
            (P, Q) where P and Q are Clifford algebra multivectors
        """
        if not (1 <= pattern_id <= 6):
            raise ValueError(f"Pattern ID must be 1-6, got {pattern_id}")

        # Canonical Six index mappings (from sedenion framework)
        index_map = {
            1: (1, 10, 4, 15),
            2: (1, 10, 5, 14),
            3: (1, 10, 6, 13),
            4: (4, 11, 1, 14),  # Pattern 4 - the anomaly
            5: (5, 10, 1, 14),
            6: (6, 9, 6, 9)
        }

        a, b, c, d = index_map[pattern_id]

        # Create multivectors using geometric product
        # In Clifford algebra: P = e_a + e_b, Q = e_c - e_d
        # The product P*Q should have zero divisor properties

        # Map to available basis vectors
        # Clifford library uses 'e1', 'e2', etc.
        max_dim = self.signature_dimension
        a_mapped = ((a - 1) % max_dim) + 1
        b_mapped = ((b - 1) % max_dim) + 1
        c_mapped = ((c - 1) % max_dim) + 1
        d_mapped = ((d - 1) % max_dim) + 1

        # Get basis blades
        e_a = self.blades[f'e{a_mapped}']
        e_b = self.blades[f'e{b_mapped}']
        e_c = self.blades[f'e{c_mapped}']
        e_d = self.blades[f'e{d_mapped}']

        # Construct P and Q
        P = e_a + e_b
        Q = e_c - e_d

        return P, Q

    def geometric_product(self, P: MultiVector, Q: MultiVector) -> MultiVector:
        """
        Compute geometric product P*Q in Clifford algebra.

        The geometric product is the fundamental operation in Clifford algebras,
        combining inner and outer products: a*b = a·b + a∧b
        """
        return P * Q

    def is_zero_divisor_clifford(self, P: MultiVector, Q: MultiVector,
                                 tolerance: float = 1e-8) -> bool:
        """
        Check if (P, Q) form a zero divisor pair in Clifford algebra.

        In Clifford algebras with degenerate metrics, zero divisors exist
        when P*Q = 0 but P ≠ 0 and Q ≠ 0.

        Args:
            P, Q: Clifford algebra multivectors
            tolerance: Numerical tolerance for zero

        Returns:
            True if P and Q form a zero divisor pair
        """
        product = self.geometric_product(P, Q)

        # Check if product is (nearly) zero
        product_norm = float(abs(product))
        p_norm = float(abs(P))
        q_norm = float(abs(Q))

        is_zero_div = (product_norm < tolerance and
                      p_norm > tolerance and
                      q_norm > tolerance)

        if is_zero_div:
            logger.info(f"Zero divisor found: |P|={p_norm:.4f}, |Q|={q_norm:.4f}, |P*Q|={product_norm:.2e}")

        return is_zero_div

    def compare_cayley_dickson_clifford(self, pattern_id: int = 1) -> Dict:
        """
        Compare the same zero divisor pattern in both frameworks.

        This demonstrates how the Canonical Six patterns appear in both:
        1. Cayley-Dickson algebras (via hypercomplex.py)
        2. Clifford algebras (this module)

        Args:
            pattern_id: Which Canonical Six pattern to compare

        Returns:
            Dictionary with results from both frameworks
        """
        # Clifford algebra computation
        P_cliff, Q_cliff = self.canonical_six_clifford(pattern_id)
        product_cliff = self.geometric_product(P_cliff, Q_cliff)
        is_zd_cliff = self.is_zero_divisor_clifford(P_cliff, Q_cliff)

        # Import Cayley-Dickson computation
        try:
            from .hypercomplex import create_hypercomplex
        except ImportError:
            # Fallback for direct script execution
            import sys
            import os
            sys.path.insert(0, os.path.dirname(__file__))
            from hypercomplex import create_hypercomplex

        # Create corresponding Cayley-Dickson elements (16D sedenions)
        index_map = {
            1: (1, 10, 4, 15),
            2: (1, 10, 5, 14),
            3: (1, 10, 6, 13),
            4: (4, 11, 1, 14),
            5: (5, 10, 1, 14),
            6: (6, 9, 6, 9)
        }

        a, b, c, d = index_map[pattern_id]

        p_coeffs = [0.0] * 16
        p_coeffs[a] = 1.0
        p_coeffs[b] = 1.0

        q_coeffs = [0.0] * 16
        q_coeffs[c] = 1.0
        q_coeffs[d] = -1.0

        P_cd = create_hypercomplex(16, p_coeffs)
        Q_cd = create_hypercomplex(16, q_coeffs)
        product_cd = P_cd * Q_cd
        is_zd_cd = abs(product_cd) < 1e-8

        return {
            "pattern_id": pattern_id,
            "clifford": {
                "signature": (self.p, self.q, self.r),
                "P": str(P_cliff),
                "Q": str(Q_cliff),
                "product": str(product_cliff),
                "product_norm": float(abs(product_cliff)),
                "is_zero_divisor": is_zd_cliff
            },
            "cayley_dickson": {
                "dimension": 16,
                "P": str(P_cd),
                "Q": str(Q_cd),
                "product": str(product_cd),
                "product_norm": float(abs(product_cd)),
                "is_zero_divisor": is_zd_cd
            },
            "frameworks_agree": is_zd_cliff == is_zd_cd
        }


def create_clifford_algebra(p: int = None, q: int = None, r: int = None,
                           dimension: int = None) -> CliffordZeroDivisors:
    """
    Factory function to create Clifford algebra instance.

    Args:
        p: Number of positive signature basis vectors
        q: Number of negative signature basis vectors
        r: Number of null (degenerate) basis vectors
        dimension: Multivector dimension (16, 32, 64, 128, 256)
            Auto-determines signature as Cl(log2(dim), 0, 0)

    Returns:
        CliffordZeroDivisors instance

    Examples:
        # By signature
        cliff = create_clifford_algebra(p=4, q=0, r=0)  # Cl(4,0,0) for 16D

        # By dimension (auto-selects signature)
        cliff = create_clifford_algebra(dimension=32)   # Auto: Cl(5,0,0)
        cliff = create_clifford_algebra(dimension=128)  # Auto: Cl(7,0,0)

    Common signatures for zero divisor analysis:
    - Cl(4,0,0): 4D Euclidean (16D multivectors)
    - Cl(5,0,0): 5D Euclidean (32D multivectors)
    - Cl(8,0,0): 8D Euclidean (256D multivectors)
    """
    if dimension is not None:
        return CliffordZeroDivisors(dimension=dimension)
    elif p is not None:
        return CliffordZeroDivisors(signature=(p, q or 0, r or 0))
    else:
        # Default to 16D
        return CliffordZeroDivisors(dimension=16)


# Convenience functions for common algebras
def sedenion_clifford_bridge(pattern_id: int = 1):
    """
    Bridge between 16D sedenions and corresponding Clifford algebra.

    Creates a Clifford algebra representation of sedenion zero divisors.
    """
    # Use Cl(4,0) as base, extend to accommodate 16D structure
    cliff = create_clifford_algebra(p=4, q=0, r=0)
    return cliff.compare_cayley_dickson_clifford(pattern_id)


if __name__ == "__main__":
    print("="*80)
    print("CLIFFORD ALGEBRAS FOR ZERO DIVISOR ANALYSIS")
    print("="*80)
    print()

    # Create Clifford algebra
    cliff = create_clifford_algebra(p=4, q=0, r=0)
    print(f"Created Clifford algebra Cl(4,0,0) - dimension {cliff.dimension}")
    print()

    # Test Canonical Six patterns
    print("Testing Canonical Six in Clifford Framework:")
    print("-" * 80)

    for pattern_id in range(1, 7):
        print(f"\nPattern {pattern_id}:")
        P, Q = cliff.canonical_six_clifford(pattern_id)
        product = cliff.geometric_product(P, Q)
        is_zd = cliff.is_zero_divisor_clifford(P, Q)

        print(f"  P = {P}")
        print(f"  Q = {Q}")
        print(f"  P*Q = {product}")
        print(f"  Is zero divisor: {is_zd}")

    print()
    print("="*80)
    print("FRAMEWORK COMPARISON: Cayley-Dickson vs Clifford")
    print("="*80)

    # Compare Pattern 4 (the anomaly) in both frameworks
    comparison = sedenion_clifford_bridge(pattern_id=4)

    print(f"\nPattern 4 - The Anomaly:")
    print(f"  Clifford: Zero divisor = {comparison['clifford']['is_zero_divisor']}")
    print(f"  Cayley-Dickson: Zero divisor = {comparison['cayley_dickson']['is_zero_divisor']}")
    print(f"  Frameworks agree: {comparison['frameworks_agree']}")
    print()
