"""
ZDTP Core Protocol - Domain-agnostic transmission

Implements the Zero Divisor Transmission Protocol for transmitting
16D input through verified mathematical gateways to 32D and 64D spaces.

The protocol provides:
1. Single gateway transmission (16D → 32D → 64D)
2. Full cascade across all six Canonical Six gateways
3. Convergence analysis measuring structural stability

User-facing value: A single trust score (convergence) that tells you if
your high-dimensional data has robust structure or is in flux.

Reference: "Framework-Independent Zero Divisor Patterns in
Higher-Dimensional Cayley-Dickson Algebras" - Chavez (2025)
"""

from typing import List, Dict, Tuple, Any, Optional

from .gateways import CANONICAL_SIX, get_gateway_pair

# Lazy imports for hypercomplex types
_Sedenion = None
_Pathion = None
_Chingon = None


def _get_hypercomplex():
    """Lazy load hypercomplex classes."""
    global _Sedenion, _Pathion, _Chingon
    if _Sedenion is None:
        from hypercomplex import Sedenion, Pathion, Chingon
        _Sedenion = Sedenion
        _Pathion = Pathion
        _Chingon = Chingon
    return _Sedenion, _Pathion, _Chingon


# Zero divisor verification tolerance
ZERO_TOLERANCE = 1e-10


class ZDTPTransmission:
    """
    Zero Divisor Transmission Protocol implementation.

    Transmits data through verified zero divisor gateways across
    dimensional spaces while maintaining mathematical verification.
    """

    def __init__(self):
        """Initialize ZDTP transmission system."""
        self._cache: Dict[str, Tuple[Any, Any]] = {}

    def transmit(self, input_16d: List[float], gateway: str) -> Dict[str, Any]:
        """
        Single gateway transmission: 16D → 32D → 64D.

        Args:
            input_16d: 16-element input vector
            gateway: Gateway pattern name (S1, S2, S3A, S3B, S4, S5)

        Returns:
            Dictionary containing:
            - state_16d: Original 16D input
            - state_32d: Transmitted 32D state
            - state_64d: Transmitted 64D state
            - gateway: Gateway used
            - zero_divisor_verified: Boolean verification status
            - product_norm: Norm of P × Q (should be ~0)

        Raises:
            ValueError: If input is not 16D or gateway is unknown
        """
        Sedenion, Pathion, Chingon = _get_hypercomplex()

        # Validate input
        if len(input_16d) != 16:
            raise ValueError(f"Input must be 16D, got {len(input_16d)}D")
        if gateway not in CANONICAL_SIX:
            valid = list(CANONICAL_SIX.keys())
            raise ValueError(f"Unknown gateway: {gateway}. Valid: {valid}")

        # Get gateway pair (cached)
        P, Q = self._get_cached_pair(gateway)

        # Verify zero divisor property
        product = P * Q
        product_norm = float(abs(product))
        if product_norm >= ZERO_TOLERANCE:
            raise ValueError(
                f"Zero divisor verification failed for {gateway}: "
                f"||P × Q|| = {product_norm:.2e} >= {ZERO_TOLERANCE:.2e}"
            )

        # Create 16D state
        state_16d = Sedenion(*input_16d)

        # Transmit 16D → 32D
        state_32d = self._to_32d(state_16d, P, Pathion)

        # Transmit 32D → 64D
        state_64d = self._to_64d(state_32d, P, Pathion, Chingon)

        return {
            "state_16d": list(state_16d.coefficients()),
            "state_32d": list(state_32d.coefficients()),
            "state_64d": list(state_64d.coefficients()),
            "gateway": gateway,
            "gateway_info": CANONICAL_SIX[gateway],
            "zero_divisor_verified": True,
            "product_norm": product_norm,
        }

    def full_cascade(self, input_16d: List[float]) -> Dict[str, Any]:
        """
        Transmit through all six gateways with convergence analysis.

        This is the core ZDTP value proposition: measure structural
        stability by comparing how data behaves across different
        mathematical pathways.

        Args:
            input_16d: 16-element input vector

        Returns:
            Dictionary containing:
            - protocol: "ZDTP"
            - version: Protocol version
            - gateways: Results for each gateway
            - convergence: Score and statistics
            - interpretation: Human-readable analysis
        """
        if len(input_16d) != 16:
            raise ValueError(f"Input must be 16D, got {len(input_16d)}D")

        results: Dict[str, Any] = {}
        magnitudes_64d: List[float] = []

        for gateway in CANONICAL_SIX:
            try:
                result = self.transmit(input_16d, gateway)

                # Compute magnitude of 64D state
                state_64d = result["state_64d"]
                magnitude = sum(x * x for x in state_64d) ** 0.5

                results[gateway] = {
                    "state_32d": result["state_32d"],
                    "state_64d": result["state_64d"],
                    "verified": result["zero_divisor_verified"],
                    "magnitude_64d": magnitude,
                    "product_norm": result["product_norm"],
                }
                magnitudes_64d.append(magnitude)

            except Exception as e:
                results[gateway] = {
                    "error": str(e),
                    "verified": False,
                }

        # Compute convergence metrics
        convergence = self._compute_convergence(magnitudes_64d)

        return {
            "protocol": "ZDTP",
            "version": "1.0",
            "input_16d": input_16d,
            "gateways": results,
            "convergence": convergence,
            "interpretation": self._interpret_convergence(convergence),
        }

    def _get_cached_pair(self, gateway: str) -> Tuple[Any, Any]:
        """Get gateway pair from cache or compute."""
        if gateway not in self._cache:
            self._cache[gateway] = get_gateway_pair(gateway)
        return self._cache[gateway]

    def _to_32d(self, state_16d: Any, gateway: Any, Pathion: type) -> Any:
        """
        Transmit 16D state to 32D via gateway interaction.

        Architecture:
        - Dims 0-15: Preserved original 16D state (lossless)
        - Dims 16-31: Gateway interaction coefficients

        Args:
            state_16d: 16D Sedenion state
            gateway: Gateway pattern P
            Pathion: Pathion class for 32D construction

        Returns:
            32D Pathion state
        """
        # Preserve original state
        original = list(state_16d.coefficients())

        # Compute gateway interaction
        interaction = state_16d * gateway
        interaction_coeffs = list(interaction.coefficients())

        # Combine: [original | interaction]
        pathion_coeffs = original + interaction_coeffs
        return Pathion(*pathion_coeffs)

    def _to_64d(self, state_32d: Any, gateway: Any, Pathion: type, Chingon: type) -> Any:
        """
        Transmit 32D state to 64D via gateway interaction.

        Architecture:
        - Dims 0-31: Preserved 32D state (lossless)
        - Dims 32-63: Extended gateway interaction

        Args:
            state_32d: 32D Pathion state
            gateway: Gateway pattern P (16D, will be promoted)
            Pathion: Pathion class for gateway promotion
            Chingon: Chingon class for 64D construction

        Returns:
            64D Chingon state
        """
        # Promote 16D gateway to 32D by padding
        gateway_coeffs = list(gateway.coefficients())
        gateway_32d = Pathion(*(gateway_coeffs + [0.0] * 16))

        # Preserve original 32D state
        original = list(state_32d.coefficients())

        # Compute extended interaction
        interaction = state_32d * gateway_32d
        interaction_coeffs = list(interaction.coefficients())

        # Combine: [original | interaction]
        chingon_coeffs = original + interaction_coeffs
        return Chingon(*chingon_coeffs)

    def _compute_convergence(self, magnitudes: List[float]) -> Dict[str, Any]:
        """
        Compute convergence metrics from 64D magnitudes.

        Convergence measures how similarly the data behaves across
        different gateway pathways. High convergence indicates
        robust structural properties.

        Args:
            magnitudes: List of 64D state magnitudes from each gateway

        Returns:
            Dictionary with score, mean, std_dev, and raw values
        """
        if not magnitudes:
            return {
                "score": 0.0,
                "mean_magnitude": 0.0,
                "std_dev": 0.0,
                "values": [],
            }

        n = len(magnitudes)
        mean_mag = sum(magnitudes) / n
        variance = sum((m - mean_mag) ** 2 for m in magnitudes) / n
        std_dev = variance ** 0.5

        # Convergence score: 1.0 = perfect agreement, 0.0 = complete disagreement
        # Normalized by mean to handle different input scales
        if mean_mag > 0:
            # Coefficient of variation inverted to get convergence
            cv = std_dev / mean_mag
            convergence_score = max(0.0, min(1.0, 1.0 - cv))
        else:
            convergence_score = 0.0

        return {
            "score": convergence_score,
            "mean_magnitude": mean_mag,
            "std_dev": std_dev,
            "values": magnitudes,
        }

    def _interpret_convergence(self, convergence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate human-readable interpretation of convergence.

        Args:
            convergence: Convergence metrics dictionary

        Returns:
            Interpretation with flags and descriptions
        """
        score = convergence["score"]

        if score > 0.8:
            level = "high"
            description = (
                "Strong structural stability. All gateways produce similar "
                "64D states, indicating robust underlying structure."
            )
        elif score > 0.5:
            level = "moderate"
            description = (
                "Moderate structural stability. Some gateway variance detected, "
                "but overall structure is reasonably consistent."
            )
        else:
            level = "low"
            description = (
                "Structural shift detected. Significant variance across gateways "
                "suggests the data is in flux or contains complex dynamics."
            )

        return {
            "level": level,
            "high_convergence": score > 0.8,
            "structural_shift": score < 0.5,
            "description": description,
            "recommendation": (
                "Structure is stable - safe for downstream processing."
                if score > 0.8
                else "Consider investigating gateway-specific behaviors."
                if score > 0.5
                else "Caution: High variance may indicate instability."
            ),
        }


# Module-level convenience function
_zdtp_instance: Optional[ZDTPTransmission] = None


def get_zdtp() -> ZDTPTransmission:
    """Get singleton ZDTP transmission instance."""
    global _zdtp_instance
    if _zdtp_instance is None:
        _zdtp_instance = ZDTPTransmission()
    return _zdtp_instance
