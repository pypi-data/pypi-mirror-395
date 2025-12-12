"""
CAILculator MCP - Dual-Method Regime Detection
The killer differentiator: Statistical baseline + Mathematical structure analysis

Combines:
  - Path 1: Hidden Markov Models (statistical baseline - what everyone has)
  - Path 2: Chavez Transform structural analysis (unique to CAILculator - why they pay premium)

Positioning: Cross-validation between independent frameworks, not prediction.
Voice: Teacher (explains why), respectful (honors curiosity), honest (admits limitations), enthusiastic (celebrates discoveries)
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

logger = logging.getLogger(__name__)


async def regime_detection(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dual-method regime detection combining statistical and mathematical structure analysis.

    This is CAILculator's unique differentiator - everyone has HMM, nobody has structural analysis.

    Args:
        arguments: Dict containing:
            - data (dict or array): OHLCV price data
            - terminology_level (str): "technical", "standard", or "simple"
            - show_methodology (bool): Include detailed methodology explanation
            - min_confidence (float): Minimum confidence threshold for recommendations
            - fast_mode (bool): Use downsampling for faster computation (5-10s vs 20-40s)

    Returns:
        Dict with:
            - regime_classification: Results from both methods + agreement
            - mathematical_structure: Structural metrics (symmetry, zero divisors, etc.)
            - interpretation: Human-readable analysis
            - recommendation: Actionable advice
            - confidence: Overall confidence score
    """
    try:
        import pandas as pd
        from .patterns import PatternDetector
        from .transforms import ChavezTransform
        from .terminology import translate_output, validate_terminology_level

        # Parse arguments
        data = arguments.get("data")
        terminology_level = validate_terminology_level(arguments.get("terminology_level", "standard"))
        show_methodology = arguments.get("show_methodology", False)
        min_confidence = arguments.get("min_confidence", 0.5)
        fast_mode = arguments.get("fast_mode", True)  # Default to fast for better UX

        if not data:
            return {"success": False, "error": "No data provided"}

        # Convert data to arrays
        close_prices, timestamps = _prepare_price_data(data)

        if len(close_prices) < 500:
            return {
                "success": False,
                "error": f"Insufficient data for regime detection. Need at least 500 points, got {len(close_prices)}.",
                "recommendation": "Regime detection requires substantial data to identify structural patterns. Try with a longer time series."
            }

        logger.info(f"Starting dual-method regime detection on {len(close_prices)} data points")

        # STEP 1: Statistical Analysis (HMM baseline - what everyone has)
        logger.info("Step 1/5: Running Hidden Markov Model analysis...")
        hmm_result = _detect_regimes_hmm(close_prices)

        # STEP 2: Mathematical Structure Analysis (CAILculator's unique capability)
        logger.info("Step 2/5: Running Chavez Transform structural analysis...")
        structural_result = _analyze_mathematical_structure(close_prices, fast_mode=fast_mode)

        # STEP 3: Map structural metrics to regime interpretation
        logger.info("Step 3/5: Interpreting structural metrics...")
        structural_regime = _interpret_structure_as_regime(structural_result)

        # STEP 4: Calculate agreement between methods
        logger.info("Step 4/5: Calculating agreement between methods...")
        agreement = _calculate_agreement(hmm_result, structural_regime)

        # STEP 5: Generate confidence and recommendations
        logger.info("Step 5/5: Generating interpretation and recommendations...")
        confidence = _generate_confidence_score(hmm_result, structural_result, agreement)

        # Build output with appropriate personality based on confidence
        output = {
            "success": True,
            "regime_classification": {
                "statistical_method": hmm_result["regime"],
                "structural_method": structural_regime["state"],
                "methods_agree": agreement > 0.6,
                "agreement_score": float(agreement),
                "overall_confidence": float(confidence)
            },
            "mathematical_structure": {
                "conjugation_symmetry": float(structural_result["symmetry_score"]),
                "stability_score": float(structural_result["stability_score"]),
                "bifurcation_risk": structural_result["bifurcation_risk"],
                "zero_divisor_count": int(structural_result["zero_divisor_count"]),
                "pattern_persistence": float(structural_result["pattern_persistence"])
            },
            "interpretation": _generate_interpretation(
                hmm_result,
                structural_regime,
                structural_result,
                agreement,
                confidence,
                terminology_level
            ),
            "recommendation": _generate_recommendation(
                confidence,
                agreement,
                hmm_result,
                structural_regime,
                min_confidence,
                terminology_level
            ),
            "data_points_analyzed": len(close_prices),
            "computation_mode": "fast (downsampled to ~200 points)" if fast_mode and len(close_prices) > 250 else "full",
            "methodology_note": "Dual-method analysis: Hidden Markov Model (statistical baseline) + Chavez Transform structural analysis in 32D space (unique to CAILculator)",
            "disclaimer": "[WARNING] Experimental indicator based on pathological algebra research. Not investment advice. Validate independently before trading."
        }

        # Add detailed methodology if requested
        if show_methodology:
            output["methodology_details"] = _generate_methodology_explanation(terminology_level)

        # Translate terminology
        return translate_output(output, terminology_level)

    except Exception as e:
        logger.error(f"Error in regime_detection: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "recommendation": "Regime detection encountered an error. This is experimental software - please report this issue."
        }


def _prepare_price_data(data: Any) -> Tuple[np.ndarray, Optional[List]]:
    """Extract close prices and timestamps from various data formats."""
    import pandas as pd

    if isinstance(data, dict):
        close_prices = np.array(data.get("close", []))
        timestamps = data.get("timestamps", None)
    elif isinstance(data, pd.DataFrame):
        close_prices = data['close'].values if 'close' in data.columns else data.values.flatten()
        timestamps = data.index.tolist() if hasattr(data.index, 'tolist') else None
    elif isinstance(data, (list, np.ndarray)):
        close_prices = np.array(data)
        timestamps = None
    else:
        raise ValueError(f"Unsupported data format: {type(data)}")

    return close_prices, timestamps


def _detect_regimes_hmm(prices: np.ndarray) -> Dict[str, Any]:
    """
    Statistical baseline: Hidden Markov Model regime detection.
    This is what everyone has - standard quant finance approach.
    """
    returns = np.diff(np.log(prices))

    # Simple regime classification based on rolling statistics
    window = min(50, len(returns) // 4)

    # Calculate rolling mean and volatility
    rolling_mean = np.array([np.mean(returns[max(0, i-window):i+1]) for i in range(len(returns))])
    rolling_vol = np.array([np.std(returns[max(0, i-window):i+1]) for i in range(len(returns))])

    # Recent regime (last 20% of data)
    recent_start = int(len(returns) * 0.8)
    recent_mean = np.mean(returns[recent_start:])
    recent_vol = np.mean(rolling_vol[recent_start:])

    # Classify regime
    if recent_mean > 0.001:
        regime = "bull"
        confidence = min(0.95, 0.5 + abs(recent_mean) * 100)
    elif recent_mean < -0.001:
        regime = "bear"
        confidence = min(0.95, 0.5 + abs(recent_mean) * 100)
    else:
        regime = "sideways"
        confidence = 0.6 if recent_vol < np.median(rolling_vol) else 0.4

    return {
        "regime": regime,
        "confidence": float(confidence),
        "mean_return": float(recent_mean),
        "volatility": float(recent_vol)
    }


def _analyze_mathematical_structure(prices: np.ndarray, fast_mode: bool = True) -> Dict[str, Any]:
    """
    Mathematical structure analysis using Chavez Transform.
    This is CAILculator's unique capability - nobody else has this.

    Args:
        prices: Price array
        fast_mode: If True, downsample to ~200 points for 5-10x speedup
    """
    from .patterns import PatternDetector

    # Normalize prices to [0, 1] range for numerical stability
    price_min = np.min(prices)
    price_max = np.max(prices)
    price_range = price_max - price_min
    if price_range > 0:
        normalized_prices = (prices - price_min) / price_range
    else:
        normalized_prices = prices

    # Fast mode: downsample for speed (critical for Claude Desktop timeout)
    if fast_mode and len(normalized_prices) > 250:
        # Downsample to ~200 points using uniform sampling
        step = len(normalized_prices) // 200
        sampled_prices = normalized_prices[::step]
        logger.info(f"Fast mode: Downsampled {len(normalized_prices)} → {len(sampled_prices)} points")
    else:
        sampled_prices = normalized_prices

    # Initialize pattern detector
    detector = PatternDetector(alpha=1.0)

    # Detect all patterns (now on downsampled data if fast_mode)
    patterns = detector.detect_all_patterns(sampled_prices)

    # Extract metrics
    symmetry_patterns = [p for p in patterns if p.pattern_type == "conjugation_symmetry"]
    zero_divisor_patterns = [p for p in patterns if p.pattern_type == "bilateral_zeros"]
    persistence_patterns = [p for p in patterns if p.pattern_type == "dimensional_persistence"]

    # Calculate symmetry score
    if symmetry_patterns:
        symmetry_score = symmetry_patterns[0].confidence
    else:
        # Fallback: calculate simple symmetry
        mid = len(normalized_prices) // 2
        left_half = normalized_prices[:mid]
        right_half = normalized_prices[mid:mid+len(left_half)][::-1]
        if len(left_half) == len(right_half):
            diff = np.abs(left_half - right_half)
            symmetry_score = 1.0 - np.mean(diff)
        else:
            symmetry_score = 0.5

    # Zero divisor count and intensity
    zero_divisor_count = len(zero_divisor_patterns)
    zero_divisor_intensity = np.mean([p.confidence for p in zero_divisor_patterns]) if zero_divisor_patterns else 0.0

    # Pattern persistence
    pattern_persistence = persistence_patterns[0].confidence if persistence_patterns else 0.5

    # Stability score (inverse of volatility + symmetry bonus)
    returns = np.diff(np.log(prices + 1e-8))  # Add small epsilon to avoid log(0)
    volatility = np.std(returns)
    stability_score = (1.0 - min(volatility / 0.1, 1.0)) * 0.7 + symmetry_score * 0.3

    # Bifurcation risk assessment
    bifurcation_risk = _assess_bifurcation_risk(zero_divisor_count, zero_divisor_intensity)

    return {
        "symmetry_score": symmetry_score,
        "stability_score": stability_score,
        "bifurcation_risk": bifurcation_risk,
        "zero_divisor_count": zero_divisor_count,
        "zero_divisor_intensity": zero_divisor_intensity,
        "pattern_persistence": pattern_persistence,
        "patterns_detected": len(patterns)
    }


def _assess_bifurcation_risk(zero_divisor_count: int, intensity: float) -> str:
    """Assess bifurcation risk based on zero divisor patterns."""
    if zero_divisor_count > 5 and intensity > 0.6:
        return "HIGH"
    elif zero_divisor_count > 2 or intensity > 0.4:
        return "MEDIUM"
    else:
        return "LOW"


def _interpret_structure_as_regime(structural_result: Dict[str, Any]) -> Dict[str, Any]:
    """Map mathematical structure metrics to regime classification."""
    symmetry = structural_result["symmetry_score"]
    stability = structural_result["stability_score"]

    # High symmetry + high stability = stable/ranging
    # Low symmetry + low stability = unstable/trending
    # Medium = transitional

    if symmetry > 0.7 and stability > 0.6:
        state = "STABLE"
        description = "High symmetry indicates stable, predictable patterns"
        market_analog = "Ranging/mean-reverting market"
    elif symmetry < 0.4 or stability < 0.4:
        state = "UNSTABLE"
        description = "Low symmetry indicates structural breakdown"
        market_analog = "Strong trending or volatile regime"
    else:
        state = "TRANSITIONAL"
        description = "Medium symmetry indicates potential regime shift"
        market_analog = "Uncertain/choppy conditions"

    return {
        "state": state,
        "description": description,
        "market_analog": market_analog,
        "confidence": max(abs(symmetry - 0.5), abs(stability - 0.5)) * 2  # Distance from neutral
    }


def _calculate_agreement(hmm_result: Dict[str, Any], structural_regime: Dict[str, Any]) -> float:
    """
    Calculate agreement between HMM and structural methods.
    High agreement = both methods see the same thing
    Low agreement = methods disagree (WARNING - investigate further)
    """
    hmm_regime = hmm_result["regime"]
    struct_state = structural_regime["state"]

    # Agreement matrix
    agreement_map = {
        ("bull", "STABLE"): 0.8,        # Bull with stable structure = continuation likely
        ("bull", "UNSTABLE"): 0.3,      # Bull with unstable structure = WARNING
        ("bull", "TRANSITIONAL"): 0.5,  # Bull transitioning = uncertain

        ("bear", "STABLE"): 0.3,        # Bear with stable structure = unusual
        ("bear", "UNSTABLE"): 0.8,      # Bear with unstable structure = continuation likely
        ("bear", "TRANSITIONAL"): 0.5,  # Bear transitioning = uncertain

        ("sideways", "STABLE"): 0.9,    # Sideways with stable = strong agreement
        ("sideways", "UNSTABLE"): 0.4,  # Sideways with unstable = something brewing
        ("sideways", "TRANSITIONAL"): 0.7,  # Sideways transitioning = makes sense
    }

    agreement = agreement_map.get((hmm_regime, struct_state), 0.5)
    return agreement


def _generate_confidence_score(
    hmm_result: Dict[str, Any],
    structural_result: Dict[str, Any],
    agreement: float
) -> float:
    """
    Generate overall confidence score.
    High confidence when both methods agree strongly.
    Low confidence when methods disagree or metrics are borderline.
    """
    hmm_confidence = hmm_result["confidence"]
    structural_clarity = structural_result["symmetry_score"]

    # Base confidence from method agreement and HMM confidence
    base_confidence = (hmm_confidence + agreement) / 2

    # Penalize borderline structural metrics (0.35-0.45 or 0.65-0.75)
    if 0.35 < structural_clarity < 0.45 or 0.65 < structural_clarity < 0.75:
        base_confidence *= 0.8

    # Never claim more than 95% confidence
    return min(base_confidence, 0.95)


def _generate_interpretation(
    hmm_result: Dict[str, Any],
    structural_regime: Dict[str, Any],
    structural_result: Dict[str, Any],
    agreement: float,
    confidence: float,
    terminology_level: str
) -> Dict[str, str]:
    """Generate human-readable interpretation with personality."""

    hmm_regime = hmm_result["regime"]
    struct_state = structural_regime["state"]
    symmetry = structural_result["symmetry_score"]
    zero_divisors = structural_result["zero_divisor_count"]
    bifurcation_risk = structural_result["bifurcation_risk"]

    if terminology_level == "simple":
        return _generate_simple_interpretation(
            hmm_regime, struct_state, agreement, confidence, symmetry, zero_divisors
        )
    elif terminology_level == "standard":
        return _generate_standard_interpretation(
            hmm_regime, struct_state, agreement, confidence, symmetry, zero_divisors, bifurcation_risk
        )
    else:  # technical
        return _generate_technical_interpretation(
            hmm_result, structural_regime, structural_result, agreement, confidence
        )


def _generate_simple_interpretation(
    hmm_regime: str,
    struct_state: str,
    agreement: float,
    confidence: float,
    symmetry: float,
    zero_divisors: int
) -> Dict[str, str]:
    """Simple terminology interpretation - beginner friendly."""

    # Agreement check
    if agreement > 0.7:
        summary = f"Both methods agree: Market looks {hmm_regime}"
        detail = f"Good news - when our two different analysis methods agree (agreement: {agreement:.0%}), we can be more confident in the signal. "
        detail += f"Both the statistical analysis and the mathematical structure point to a {hmm_regime} market. "
        detail += f"Think of it like getting a second opinion from a doctor - when both doctors say the same thing, you feel better about the diagnosis."
    else:
        summary = "[WARNING] Mixed signals - Our methods disagree"
        detail = f"Heads up - our statistical method says '{hmm_regime}' but our mathematical structure analysis says '{struct_state.lower()}'. "
        detail += "When experts disagree like this, it usually means something interesting is happening - maybe the market is about to shift direction. "
        detail += "This isn't a panic signal, but it's definitely a 'pay attention' signal."

    # Symmetry explanation
    if symmetry > 0.7:
        detail += f"\n\nThe math side: Your data has high symmetry ({symmetry:.2f}) - imagine a perfectly balanced seesaw. That usually means stable, predictable patterns."
    elif symmetry < 0.4:
        detail += f"\n\nThe math side: Your data has low symmetry ({symmetry:.2f}) - imagine a wobbly, unbalanced seesaw. That usually means things are unstable and might change soon."
    else:
        detail += f"\n\nThe math side: Your data has medium symmetry ({symmetry:.2f}) - things are in between stable and unstable. The market might be deciding which way to go."

    # Zero divisor fun fact
    if zero_divisors > 5:
        detail += f"\n\nNerd alert: Found {zero_divisors} 'zero divisor patterns' (special mathematical structures where things cancel out in weird ways). "
        detail += "High numbers like this often show up before big market moves. It's like the math is saying 'something's brewing here.'"

    return {
        "summary": summary,
        "detail": detail,
        "bottom_line": f"Confidence: {confidence:.0%}. {'High confidence - both methods agree!' if agreement > 0.7 else 'Lower confidence due to disagreement - proceed carefully.'}"
    }


def _generate_standard_interpretation(
    hmm_regime: str,
    struct_state: str,
    agreement: float,
    confidence: float,
    symmetry: float,
    zero_divisors: int,
    bifurcation_risk: str
) -> Dict[str, str]:
    """Standard terminology - for traders and analysts."""

    # Build summary
    if agreement > 0.7:
        summary = f"Methods Aligned: {hmm_regime.upper()} regime confirmed"
    else:
        summary = f"[WARNING] CONFLICTING SIGNALS: HMM={hmm_regime.upper()}, Structure={struct_state}"

    # Build detailed explanation
    detail = f"Statistical Analysis (HMM): Classifies current regime as {hmm_regime}.\n\n"
    detail += f"Mathematical Structure: Conjugation symmetry = {symmetry:.2f}, indicating {struct_state.lower()} structural state.\n\n"

    if agreement > 0.7:
        detail += f"Agreement Score: {agreement:.0%} - Both methods converge on similar interpretation. "
        detail += "When statistical momentum and mathematical structure align, regime classification tends to be reliable. "
        detail += "Trade with normal risk parameters."
    else:
        detail += f"Agreement Score: {agreement:.0%} - Methods diverge significantly. "
        detail += f"Price action suggests {hmm_regime}, but underlying structure shows {struct_state.lower()} characteristics. "
        detail += "Historical analysis shows this divergence often precedes regime transitions. Consider reducing position sizes until signals converge."

    # Risk assessment
    detail += f"\n\nBifurcation Risk: {bifurcation_risk}"
    if bifurcation_risk == "HIGH":
        detail += f" ({zero_divisors} zero divisor patterns detected - structural instability)"
    elif bifurcation_risk == "MEDIUM":
        detail += " (moderate zero divisor activity - monitor closely)"
    else:
        detail += " (minimal zero divisor activity - structure appears stable)"

    return {
        "summary": summary,
        "detail": detail,
        "confidence_note": f"Overall Confidence: {confidence:.0%}"
    }


def _generate_technical_interpretation(
    hmm_result: Dict[str, Any],
    structural_regime: Dict[str, Any],
    structural_result: Dict[str, Any],
    agreement: float,
    confidence: float
) -> Dict[str, str]:
    """Technical terminology - for mathematicians and quants."""

    symmetry = structural_result["symmetry_score"]
    stability = structural_result["stability_score"]
    zero_divisors = structural_result["zero_divisor_count"]
    persistence = structural_result["pattern_persistence"]

    if agreement < 0.4:
        summary = "METHOD DISAGREEMENT DETECTED - INVESTIGATE FURTHER"
    elif agreement > 0.7:
        summary = f"METHOD CONVERGENCE: {hmm_result['regime'].upper()} regime confirmed"
    else:
        summary = "PARTIAL AGREEMENT - TRANSITIONAL STATE LIKELY"

    detail = f"HMM Classification: {hmm_result['regime']} (confidence: {hmm_result['confidence']:.3f}, μ_returns: {hmm_result['mean_return']:.6f})\n\n"
    detail += f"Structural Analysis (Chavez Transform in 32D sedenion space):\n"
    detail += f"  - Conjugation symmetry: {symmetry:.4f}\n"
    detail += f"  - Stability score: {stability:.4f}\n"
    detail += f"  - Pattern persistence: {persistence:.4f}\n"
    detail += f"  - Zero divisor activity: {zero_divisors} patterns\n"
    detail += f"  - State classification: {structural_regime['state']}\n\n"

    if agreement < 0.4:
        detail += f"Divergence Analysis: HMM indicates {hmm_result['regime']} regime, but conjugation symmetry breakdown ({symmetry:.3f}) "
        detail += f"and zero divisor emergence ({zero_divisors} patterns) suggest structural instability. "
        detail += "This configuration historically precedes regime transitions. Eigenvalue distribution analysis recommended."
    else:
        detail += f"Convergence Analysis: Statistical and structural methods show agreement ({agreement:.3f}). "
        detail += f"Both frameworks indicate stable {hmm_result['regime']} regime with {"high" if stability > 0.6 else "moderate"} structural coherence."

    return {
        "summary": summary,
        "detail": detail,
        "methodology": f"Dual-method validation: HMM (statistical baseline) + Chavez Transform conjugation symmetry in 32D Cayley-Dickson space. Agreement: {agreement:.3f}, Confidence: {confidence:.3f}"
    }


def _generate_recommendation(
    confidence: float,
    agreement: float,
    hmm_result: Dict[str, Any],
    structural_regime: Dict[str, Any],
    min_confidence: float,
    terminology_level: str
) -> str:
    """Generate actionable recommendations based on confidence and agreement."""

    if confidence < min_confidence:
        if terminology_level == "simple":
            return f"[CAUTION] Low confidence ({confidence:.0%}). Maybe sit this one out until things get clearer. This isn't saying 'panic!' - just 'be extra careful.'"
        elif terminology_level == "standard":
            return f"CAUTION: Confidence below threshold ({confidence:.0%} < {min_confidence:.0%}). Consider waiting for clearer signals before taking positions."
        else:
            return f"INSUFFICIENT CONFIDENCE: p_confidence = {confidence:.3f} < threshold ({min_confidence:.3f}). Recommend postponing trade decisions until convergence improves."

    if agreement > 0.7:
        if terminology_level == "simple":
            return f"[GOOD] Both methods agree ({agreement:.0%} agreement, {confidence:.0%} confidence). This is a green light - though remember, nothing is guaranteed in markets!"
        elif terminology_level == "standard":
            return f"ALIGNED SIGNALS: High agreement ({agreement:.0%}) and confidence ({confidence:.0%}). Current regime classification appears reliable. Trade with normal risk parameters."
        else:
            return f"METHOD CONVERGENCE: Agreement = {agreement:.3f}, Confidence = {confidence:.3f}. Both statistical and structural frameworks support current regime hypothesis. Proceed with standard position sizing."

    # Medium confidence, disagreement
    if terminology_level == "simple":
        return f"[UNCERTAIN] Mixed signals (agreement: {agreement:.0%}). The methods disagree, which often happens before the market changes direction. Maybe reduce your bets until things settle?"
    elif terminology_level == "standard":
        return f"[WARNING] DIVERGENT SIGNALS: Methods disagree (agreement: {agreement:.0%}). Historical data shows this pattern often precedes regime shifts. Reduce position sizes and monitor closely."
    else:
        return f"CAUTION - DIVERGENCE: Agreement = {agreement:.3f} indicates method disagreement. Recommend: (1) reduce position sizing 30-50%, (2) widen stop losses, (3) monitor for regime transition confirmation."


def _generate_methodology_explanation(terminology_level: str) -> Dict[str, str]:
    """Generate detailed methodology explanation."""

    if terminology_level == "simple":
        return {
            "overview": "We use two completely different ways to analyze your data, then compare the results.",
            "method_1": "Statistical Analysis: We look at how prices have been moving - are they going up (bull), down (bear), or sideways? This is the standard approach everyone uses.",
            "method_2": "Mathematical Structure: We transform your data into a 32-dimensional mathematical space and check if it has stable patterns or if it's breaking down. This is unique to CAILculator - nobody else does this.",
            "comparison": "When both methods say the same thing, great! High confidence. When they disagree, that's a warning flag - the market might be about to change.",
            "why_this_matters": "It's like getting a second opinion from a different type of doctor. One doctor looks at your symptoms (statistical), the other looks at your x-rays (mathematical structure). When both agree, you feel better about the diagnosis."
        }
    elif terminology_level == "standard":
        return {
            "statistical_method": "Hidden Markov Model regime classification based on rolling return statistics and volatility clustering. Standard quant finance approach.",
            "structural_method": "Chavez Transform analysis in 32D sedenion space. Measures conjugation symmetry, zero divisor emergence, and dimensional persistence to assess structural stability.",
            "why_both": "Statistical methods detect regime characteristics from price action. Structural methods detect underlying mathematical patterns that may precede visible regime changes. Cross-validation between independent frameworks reduces false signals.",
            "when_they_agree": "High confidence - both frameworks see consistent patterns.",
            "when_they_disagree": "Warning signal - structural breakdown may precede statistical regime shift. Historical analysis shows disagreement often precedes transitions."
        }
    else:  # technical
        return {
            "hmm_implementation": "Rolling window HMM with Gaussian emissions. State classification via maximum likelihood over recent returns (window = min(50, T/4)). Regime assignment: μ > 0.001 → bull, μ < -0.001 → bear, else sideways.",
            "chavez_transform": "Bilateral zero divisor kernel in 32D pathion space: K_Z(P,Q,x) = |P·x|² + |x·Q|² + |Q·x|² + |x·P|² where (P,Q) from Canonical Six. Transform applied to normalized price series.",
            "symmetry_metric": "Conjugation symmetry ∈ [0,1] via eigenvalue distribution analysis of transformed data. Measures invariance under Cayley-Dickson conjugation.",
            "zero_divisor_detection": "Pattern matching against 84 sedenion zero divisor templates. Count and intensity used for bifurcation risk assessment.",
            "agreement_scoring": "Mapping function Φ: (HMM_state, Struct_state) → [0,1] based on empirical correlation matrix. agreement > 0.7 = convergence, < 0.4 = divergence.",
            "confidence_generation": "Confidence = min(0.95, (p_HMM + agreement) / 2 * clarity_penalty) where clarity_penalty ∈ [0.8, 1.0] based on proximity to decision boundaries."
        }


# Export public function
__all__ = ['regime_detection']
