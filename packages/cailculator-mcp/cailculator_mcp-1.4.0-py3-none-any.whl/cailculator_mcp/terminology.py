"""
CAILculator MCP - Financial Terminology Translation
Maps mathematical concepts to financial/trading language
Three levels: technical, standard, simple
"""

from typing import Dict, Any


# Core terminology mappings
FINANCIAL_GLOSSARY = {
    # Pattern detection terms
    "conjugation_symmetry": {
        "technical": "Conjugation symmetry detection (eigenvalue stability in hypercomplex space)",
        "standard": "Mean reversion strength indicator",
        "simple": "How strongly price returns to average"
    },
    "bilateral_zeros": {
        "technical": "Bilateral zero divisor detection in sedenion/pathion algebras",
        "standard": "Volatility regime shift signals",
        "simple": "Major market mood changes"
    },
    "dimensional_persistence": {
        "technical": "Cross-dimensional pattern stability (16D→32D→64D Cayley-Dickson)",
        "standard": "Pattern stability across timeframes",
        "simple": "Patterns that work on multiple chart timeframes (daily, weekly, monthly)"
    },

    # Transform and convergence
    "transform_convergence": {
        "technical": "Chavez Transform L² convergence with alpha-parametrized damping",
        "standard": "Analysis confidence score",
        "simple": "How sure we are about the results"
    },
    "chavez_transform": {
        "technical": "Zero-divisor weighted integral transform in pathion space",
        "standard": "Pattern-weighted data analysis",
        "simple": "Smart way to find hidden patterns in data"
    },
    "transform_value": {
        "technical": "Functional transform magnitude ||T_α(f)||",
        "standard": "Pattern strength score",
        "simple": "How strong the pattern is"
    },

    # Zero divisors and algebra
    "zero_divisor": {
        "technical": "Non-zero elements P, Q where P×Q = 0 in non-associative algebra",
        "standard": "Structural weakness point in data",
        "simple": "Special relationship where things cancel out"
    },
    "canonical_six": {
        "technical": "Six fundamental zero divisor patterns in 16D sedenion space",
        "standard": "Core pattern templates",
        "simple": "Six basic patterns that repeat everywhere"
    },
    "sedenion": {
        "technical": "16-dimensional Cayley-Dickson algebra (non-associative)",
        "standard": "16-dimensional pattern space",
        "simple": "Way to analyze 16 variables at once"
    },
    "pathion": {
        "technical": "32-dimensional Cayley-Dickson algebra extension",
        "standard": "32-dimensional pattern space",
        "simple": "Way to analyze 32 variables at once"
    },

    # Pattern characteristics
    "pattern_confidence": {
        "technical": "Statistical significance p < 0.05 with bootstrap validation",
        "standard": "Pattern reliability score",
        "simple": "How likely the pattern is real vs random chance"
    },
    "cross_block": {
        "technical": "Inter-block zero divisor patterns (16D→32D inheritance)",
        "standard": "Multi-timeframe correlation",
        "simple": "Patterns connecting different time periods"
    },
    "hyperwormhole": {
        "technical": "Dimensional invariant zero divisor (e₆ × e₉ = 0 across all dimensions)",
        "standard": "Universal pattern anchor",
        "simple": "Pattern that works everywhere"
    },

    # Analysis types
    "pattern_detection": {
        "technical": "Structural pattern identification via transform eigenspace analysis",
        "standard": "Finding repeating patterns in data",
        "simple": "Looking for things that happen over and over"
    },
    "regime_detection": {
        "technical": "Hidden Markov model state classification with volatility clustering",
        "standard": "Market phase identification (bull/bear/sideways)",
        "simple": "Figuring out if market is going up, down, or sideways"
    },
    "anomaly_detection": {
        "technical": "Outlier identification via Mahalanobis distance in transform space",
        "standard": "Unusual event detection",
        "simple": "Finding weird stuff that doesn't fit the pattern"
    },

    # Validation and quality
    "norm_squared": {
        "technical": "Euclidean norm squared: ||x||² = Σᵢ xᵢ²",
        "standard": "Magnitude squared",
        "simple": "Size of the number"
    },
    "product_norm": {
        "technical": "||P × Q|| for zero divisor validation (expect < 1e-10)",
        "standard": "Multiplication result size",
        "simple": "Result after multiplying two numbers"
    },
    "convergence_rate": {
        "technical": "Proportion of sequences satisfying |aₙ - L| < ε for large n",
        "standard": "How fast analysis settles down",
        "simple": "Speed of getting to final answer"
    },

    # Signal interpretation
    "bullish": {
        "technical": "Positive momentum with directional bias > 0",
        "standard": "Upward price trend expected",
        "simple": "Price likely going up"
    },
    "bearish": {
        "technical": "Negative momentum with directional bias < 0",
        "standard": "Downward price trend expected",
        "simple": "Price likely going down"
    },
    "neutral": {
        "technical": "Zero momentum with non-directional stochastic drift",
        "standard": "No clear trend",
        "simple": "Price going sideways"
    },
    "overbought": {
        "technical": "RSI > 70 or price > +2σ Bollinger Band",
        "standard": "Price extended above normal range",
        "simple": "Price too high, might drop soon"
    },
    "oversold": {
        "technical": "RSI < 30 or price < -2σ Bollinger Band",
        "standard": "Price extended below normal range",
        "simple": "Price too low, might bounce up"
    },

    # Risk and volatility
    "volatility": {
        "technical": "Standard deviation of log returns: σ = √(Var(log(Pₜ/Pₜ₋₁)))",
        "standard": "Price movement variability",
        "simple": "How jumpy the price is"
    },
    "value_at_risk": {
        "technical": "VaR(α) = -inf{x : P(X ≤ x) ≥ α} for loss distribution",
        "standard": "Maximum expected loss at confidence level",
        "simple": "Worst case loss we might see"
    },
    "sharpe_ratio": {
        "technical": "(E[R] - Rₓ) / σ_R where Rₓ is risk-free rate",
        "standard": "Risk-adjusted return measure",
        "simple": "Return per unit of risk taken"
    },
    "max_drawdown": {
        "technical": "max_t(max_s≤t(X_s) - X_t) / max_s≤t(X_s)",
        "standard": "Peak-to-trough decline",
        "simple": "Biggest drop from top to bottom"
    },

    # Indicators
    "relative_strength_index": {
        "technical": "RSI = 100 - 100/(1 + RS) where RS = avg_gain/avg_loss over n periods",
        "standard": "Momentum oscillator (0-100 scale)",
        "simple": "Measures if price went up or down recently"
    },
    "moving_average_convergence_divergence": {
        "technical": "MACD = EMA₁₂ - EMA₂₆; Signal = EMA₉(MACD)",
        "standard": "Trend-following momentum indicator",
        "simple": "Shows if uptrend or downtrend is getting stronger"
    },
    "bollinger_bands": {
        "technical": "BBands = SMA_n ± k×σ_n where σ_n is n-period std dev",
        "standard": "Volatility bands around moving average",
        "simple": "Upper and lower boundaries showing price range"
    },
}


# Field name mappings (for renaming keys in output)
FIELD_MAPPINGS = {
    "technical": {
        # Keep original field names
    },
    "standard": {
        "conjugation_symmetry": "mean_reversion",
        "bilateral_zeros": "regime_shifts",
        "dimensional_persistence": "timeframe_stability",
        "transform_convergence": "confidence_score",
        "chavez_transform": "pattern_analysis",
        "zero_divisor": "structural_weakness",
        "canonical_six": "core_patterns",
    },
    "simple": {
        "conjugation_symmetry": "return_to_average",
        "bilateral_zeros": "mood_changes",
        "dimensional_persistence": "pattern_consistency",
        "transform_convergence": "certainty",
        "chavez_transform": "pattern_finder",
        "zero_divisor": "cancellation_point",
        "canonical_six": "basic_patterns",
    }
}


def translate_term(term: str, level: str = "standard") -> str:
    """
    Translate a single technical term to specified level.

    Args:
        term: Technical term to translate
        level: "technical", "standard", or "simple"

    Returns:
        Translated term
    """
    if level == "technical":
        return term

    term_lower = term.lower().replace(" ", "_")

    # Check if term is in glossary
    if term_lower in FINANCIAL_GLOSSARY:
        return FINANCIAL_GLOSSARY[term_lower].get(level, term)

    return term


def translate_output(result_dict: Dict[str, Any], level: str = "standard") -> Dict[str, Any]:
    """
    Translate entire tool output to specified terminology level.

    Args:
        result_dict: Tool output dictionary
        level: "technical", "standard", or "simple"

    Returns:
        Translated dictionary with appropriate field names and descriptions
    """
    if level == "technical":
        return result_dict  # No translation needed

    translated = {}

    # Get field mappings for this level
    field_map = FIELD_MAPPINGS.get(level, {})

    for key, value in result_dict.items():
        # Translate key name if mapping exists
        new_key = field_map.get(key, key)

        # Recursively translate nested dicts
        if isinstance(value, dict):
            translated[new_key] = translate_output(value, level)
        elif isinstance(value, str):
            # Translate string values that might be technical terms
            translated[new_key] = translate_term(value, level)
        else:
            translated[new_key] = value

    return translated


def add_terminology_context(result_dict: Dict[str, Any], level: str = "standard") -> Dict[str, Any]:
    """
    Add explanatory context to result based on terminology level.

    Args:
        result_dict: Tool output dictionary
        level: "technical", "standard", or "simple"

    Returns:
        Dictionary with added explanations
    """
    result = result_dict.copy()

    # Add level-appropriate explanations
    if level == "simple":
        result["_explanation"] = (
            "This analysis looks for patterns in your data. "
            "We check how prices move and find repeating behaviors. "
            "Results are shown in plain English."
        )
    elif level == "standard":
        result["_explanation"] = (
            "Professional technical analysis using industry-standard terminology. "
            "Indicators measure momentum, trend strength, and volatility. "
            "Suitable for traders and financial analysts."
        )
    else:  # technical
        result["_explanation"] = (
            "Mathematical analysis using Cayley-Dickson algebra and zero divisor theory. "
            "Full technical notation preserved for academic and research contexts."
        )

    return result


def get_terminology_help(level: str = "standard") -> Dict[str, str]:
    """
    Get glossary of terms for specified level.

    Args:
        level: "technical", "standard", or "simple"

    Returns:
        Dictionary mapping terms to definitions at that level
    """
    glossary = {}

    for term, definitions in FINANCIAL_GLOSSARY.items():
        glossary[term] = definitions.get(level, definitions.get("standard", term))

    return glossary


def validate_terminology_level(level: str) -> str:
    """
    Validate and normalize terminology level.

    Args:
        level: User-provided level

    Returns:
        Normalized level ("technical", "standard", or "simple")
    """
    level_lower = level.lower().strip()

    if level_lower in ["technical", "tech", "advanced", "academic"]:
        return "technical"
    elif level_lower in ["simple", "basic", "beginner", "plain", "easy"]:
        return "simple"
    else:
        return "standard"  # Default
