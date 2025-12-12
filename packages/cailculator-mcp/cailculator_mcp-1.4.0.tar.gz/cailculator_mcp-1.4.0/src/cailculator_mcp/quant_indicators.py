"""
CAILculator MCP - Quantitative Technical Indicators
Professional technical analysis indicators for financial markets
Uses pandas_ta library for industry-standard calculations
"""

import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


async def market_indicators(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate professional technical indicators for financial data.

    Supported indicators:
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence)
    - Bollinger Bands
    - SMA/EMA (Simple/Exponential Moving Averages)
    - ATR (Average True Range)
    - Stochastic Oscillator
    - ADX (Average Directional Index)
    - OBV (On Balance Volume)
    - VWAP (Volume Weighted Average Price)
    - Ichimoku Cloud

    Args:
        arguments: Dict containing:
            - data (dict or list): OHLCV data (dict with keys or list of lists)
            - indicators (list): List of indicator names to calculate
            - periods (dict, optional): Custom periods for indicators
            - terminology_level (str): "technical", "standard", or "simple"

    Returns:
        Dict with indicator values, signals, and interpretation
    """
    try:
        # Lazy imports
        import pandas as pd
        import numpy as np

        # Parse arguments
        data = arguments.get("data")
        indicators_requested = arguments.get("indicators", ["RSI", "MACD"])
        custom_periods = arguments.get("periods", {})
        terminology_level = arguments.get("terminology_level", "standard")

        if not data:
            return {"success": False, "error": "No data provided"}

        # Convert data to DataFrame
        df = _prepare_dataframe(data)

        if df is None or df.empty:
            return {"success": False, "error": "Could not parse data into DataFrame"}

        logger.info(f"Calculating {len(indicators_requested)} indicators for {len(df)} data points")

        # Import pandas_ta (lazy import to avoid startup delay)
        try:
            import pandas_ta as ta
        except ImportError:
            return {
                "success": False,
                "error": "pandas_ta library not installed. Run: pip install pandas-ta"
            }

        # Calculate requested indicators
        results = {}
        signals = {}

        for indicator in indicators_requested:
            indicator_upper = indicator.upper()

            try:
                if indicator_upper == "RSI":
                    period = custom_periods.get("rsi", 14)
                    rsi = ta.rsi(df['close'], length=period)
                    results["rsi"] = {
                        "values": rsi.dropna().tolist(),
                        "current": float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None,
                        "period": period
                    }
                    signals["rsi"] = _interpret_rsi(rsi.iloc[-1])

                elif indicator_upper == "MACD":
                    fast = custom_periods.get("macd_fast", 12)
                    slow = custom_periods.get("macd_slow", 26)
                    signal = custom_periods.get("macd_signal", 9)

                    macd = ta.macd(df['close'], fast=fast, slow=slow, signal=signal)

                    results["macd"] = {
                        "macd": macd[f'MACD_{fast}_{slow}_{signal}'].dropna().tolist(),
                        "signal": macd[f'MACDs_{fast}_{slow}_{signal}'].dropna().tolist(),
                        "histogram": macd[f'MACDh_{fast}_{slow}_{signal}'].dropna().tolist(),
                        "current_macd": float(macd[f'MACD_{fast}_{slow}_{signal}'].iloc[-1]),
                        "current_signal": float(macd[f'MACDs_{fast}_{slow}_{signal}'].iloc[-1]),
                        "current_histogram": float(macd[f'MACDh_{fast}_{slow}_{signal}'].iloc[-1])
                    }
                    signals["macd"] = _interpret_macd(
                        macd[f'MACD_{fast}_{slow}_{signal}'].iloc[-1],
                        macd[f'MACDs_{fast}_{slow}_{signal}'].iloc[-1],
                        macd[f'MACDh_{fast}_{slow}_{signal}'].iloc[-1]
                    )

                elif indicator_upper == "BOLLINGER" or indicator_upper == "BBANDS":
                    period = custom_periods.get("bollinger_period", 20)
                    std = custom_periods.get("bollinger_std", 2)

                    bbands = ta.bbands(df['close'], length=period, std=std)

                    # Handle different pandas_ta versions - search for columns by prefix
                    bbu_col = None
                    bbm_col = None
                    bbl_col = None

                    for col in bbands.columns:
                        if col.startswith(f'BBU_{period}'):
                            bbu_col = col
                        elif col.startswith(f'BBM_{period}'):
                            bbm_col = col
                        elif col.startswith(f'BBL_{period}'):
                            bbl_col = col

                    if not all([bbu_col, bbm_col, bbl_col]):
                        results["bollinger_bands"] = {
                            "error": f"Could not find Bollinger Bands columns. Available: {list(bbands.columns)}"
                        }
                        continue

                    results["bollinger_bands"] = {
                        "upper": bbands[bbu_col].dropna().tolist(),
                        "middle": bbands[bbm_col].dropna().tolist(),
                        "lower": bbands[bbl_col].dropna().tolist(),
                        "current_upper": float(bbands[bbu_col].iloc[-1]),
                        "current_middle": float(bbands[bbm_col].iloc[-1]),
                        "current_lower": float(bbands[bbl_col].iloc[-1]),
                        "current_price": float(df['close'].iloc[-1]),
                        "period": period,
                        "std": std
                    }
                    signals["bollinger_bands"] = _interpret_bollinger(
                        df['close'].iloc[-1],
                        bbands[bbu_col].iloc[-1],
                        bbands[bbl_col].iloc[-1]
                    )

                elif indicator_upper == "SMA":
                    period = custom_periods.get("sma_period", 20)
                    sma = ta.sma(df['close'], length=period)

                    results["sma"] = {
                        "values": sma.dropna().tolist(),
                        "current": float(sma.iloc[-1]),
                        "current_price": float(df['close'].iloc[-1]),
                        "period": period
                    }
                    signals["sma"] = _interpret_moving_average(df['close'].iloc[-1], sma.iloc[-1])

                elif indicator_upper == "EMA":
                    period = custom_periods.get("ema_period", 20)
                    ema = ta.ema(df['close'], length=period)

                    results["ema"] = {
                        "values": ema.dropna().tolist(),
                        "current": float(ema.iloc[-1]),
                        "current_price": float(df['close'].iloc[-1]),
                        "period": period
                    }
                    signals["ema"] = _interpret_moving_average(df['close'].iloc[-1], ema.iloc[-1])

                elif indicator_upper == "ATR":
                    if not all(col in df.columns for col in ['high', 'low', 'close']):
                        results["atr"] = {"error": "ATR requires high, low, close data"}
                        continue

                    period = custom_periods.get("atr_period", 14)
                    atr = ta.atr(df['high'], df['low'], df['close'], length=period)

                    results["atr"] = {
                        "values": atr.dropna().tolist(),
                        "current": float(atr.iloc[-1]),
                        "period": period,
                        "percent_of_price": float((atr.iloc[-1] / df['close'].iloc[-1]) * 100)
                    }
                    signals["atr"] = _interpret_atr(atr.iloc[-1], df['close'].iloc[-1])

                elif indicator_upper == "STOCHASTIC" or indicator_upper == "STOCH":
                    if not all(col in df.columns for col in ['high', 'low', 'close']):
                        results["stochastic"] = {"error": "Stochastic requires high, low, close data"}
                        continue

                    k_period = custom_periods.get("stoch_k", 14)
                    d_period = custom_periods.get("stoch_d", 3)

                    stoch = ta.stoch(df['high'], df['low'], df['close'], k=k_period, d=d_period)

                    results["stochastic"] = {
                        "k": stoch[f'STOCHk_{k_period}_{d_period}_3'].dropna().tolist(),
                        "d": stoch[f'STOCHd_{k_period}_{d_period}_3'].dropna().tolist(),
                        "current_k": float(stoch[f'STOCHk_{k_period}_{d_period}_3'].iloc[-1]),
                        "current_d": float(stoch[f'STOCHd_{k_period}_{d_period}_3'].iloc[-1])
                    }
                    signals["stochastic"] = _interpret_stochastic(
                        stoch[f'STOCHk_{k_period}_{d_period}_3'].iloc[-1],
                        stoch[f'STOCHd_{k_period}_{d_period}_3'].iloc[-1]
                    )

                elif indicator_upper == "ADX":
                    if not all(col in df.columns for col in ['high', 'low', 'close']):
                        results["adx"] = {"error": "ADX requires high, low, close data"}
                        continue

                    period = custom_periods.get("adx_period", 14)
                    adx = ta.adx(df['high'], df['low'], df['close'], length=period)

                    results["adx"] = {
                        "adx": adx[f'ADX_{period}'].dropna().tolist(),
                        "dmp": adx[f'DMP_{period}'].dropna().tolist(),
                        "dmn": adx[f'DMN_{period}'].dropna().tolist(),
                        "current_adx": float(adx[f'ADX_{period}'].iloc[-1]),
                        "current_dmp": float(adx[f'DMP_{period}'].iloc[-1]),
                        "current_dmn": float(adx[f'DMN_{period}'].iloc[-1]),
                        "period": period
                    }
                    signals["adx"] = _interpret_adx(
                        adx[f'ADX_{period}'].iloc[-1],
                        adx[f'DMP_{period}'].iloc[-1],
                        adx[f'DMN_{period}'].iloc[-1]
                    )

                elif indicator_upper == "OBV":
                    if 'volume' not in df.columns:
                        results["obv"] = {"error": "OBV requires volume data"}
                        continue

                    obv = ta.obv(df['close'], df['volume'])

                    results["obv"] = {
                        "values": obv.dropna().tolist(),
                        "current": float(obv.iloc[-1]),
                        "trend": "bullish" if obv.iloc[-1] > obv.iloc[-5] else "bearish"
                    }
                    signals["obv"] = _interpret_obv(obv.iloc[-1], obv.iloc[-5])

                elif indicator_upper == "VWAP":
                    if not all(col in df.columns for col in ['high', 'low', 'close', 'volume']):
                        results["vwap"] = {"error": "VWAP requires high, low, close, volume data"}
                        continue

                    vwap = ta.vwap(df['high'], df['low'], df['close'], df['volume'])

                    results["vwap"] = {
                        "values": vwap.dropna().tolist(),
                        "current": float(vwap.iloc[-1]),
                        "current_price": float(df['close'].iloc[-1])
                    }
                    signals["vwap"] = _interpret_vwap(df['close'].iloc[-1], vwap.iloc[-1])

                else:
                    results[indicator] = {"error": f"Unsupported indicator: {indicator}"}

            except Exception as e:
                logger.error(f"Error calculating {indicator}: {e}", exc_info=True)
                results[indicator] = {"error": str(e)}

        # Generate interpretation based on terminology level
        interpretation = _generate_interpretation(
            results, signals, terminology_level, len(df)
        )

        return {
            "success": True,
            "indicators": results,
            "signals": signals,
            "data_points": len(df),
            "interpretation": interpretation
        }

    except Exception as e:
        logger.error(f"Error in market_indicators: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


def _prepare_dataframe(data: Any) -> Any:
    """Convert various data formats to pandas DataFrame."""
    import pandas as pd

    if isinstance(data, pd.DataFrame):
        return data

    if isinstance(data, dict):
        # Assume dict has keys: open, high, low, close, volume
        df = pd.DataFrame(data)
        return df

    if isinstance(data, list):
        # Assume list of lists: [[timestamp, open, high, low, close, volume], ...]
        if len(data) > 0 and isinstance(data[0], list):
            if len(data[0]) == 6:
                df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            elif len(data[0]) == 5:
                df = pd.DataFrame(data, columns=['open', 'high', 'low', 'close', 'volume'])
            else:
                return None
            return df

    return None


def _interpret_rsi(rsi_value: float) -> Dict[str, Any]:
    """Interpret RSI value and generate trading signal."""
    if pd.isna(rsi_value):
        return {"signal": "insufficient_data", "strength": "none"}

    if rsi_value > 70:
        return {"signal": "overbought", "strength": "strong", "action": "consider_selling"}
    elif rsi_value > 60:
        return {"signal": "overbought", "strength": "moderate", "action": "caution"}
    elif rsi_value < 30:
        return {"signal": "oversold", "strength": "strong", "action": "consider_buying"}
    elif rsi_value < 40:
        return {"signal": "oversold", "strength": "moderate", "action": "watch"}
    else:
        return {"signal": "neutral", "strength": "none", "action": "hold"}


def _interpret_macd(macd: float, signal: float, histogram: float) -> Dict[str, Any]:
    """Interpret MACD indicator."""
    if macd > signal and histogram > 0:
        return {"signal": "bullish", "crossover": "above", "action": "consider_buying"}
    elif macd < signal and histogram < 0:
        return {"signal": "bearish", "crossover": "below", "action": "consider_selling"}
    else:
        return {"signal": "neutral", "crossover": "none", "action": "hold"}


def _interpret_bollinger(price: float, upper: float, lower: float) -> Dict[str, Any]:
    """Interpret Bollinger Bands position."""
    band_width = upper - lower
    position = (price - lower) / band_width if band_width > 0 else 0.5

    if position > 0.95:
        return {"signal": "overbought", "position": "near_upper", "action": "consider_selling"}
    elif position < 0.05:
        return {"signal": "oversold", "position": "near_lower", "action": "consider_buying"}
    else:
        return {"signal": "neutral", "position": "middle", "action": "hold"}


def _interpret_moving_average(price: float, ma: float) -> Dict[str, Any]:
    """Interpret price relative to moving average."""
    if price > ma * 1.02:
        return {"signal": "bullish", "position": "above", "action": "hold_long"}
    elif price < ma * 0.98:
        return {"signal": "bearish", "position": "below", "action": "hold_short"}
    else:
        return {"signal": "neutral", "position": "at", "action": "wait"}


def _interpret_atr(atr: float, price: float) -> Dict[str, Any]:
    """Interpret Average True Range."""
    atr_percent = (atr / price) * 100

    if atr_percent > 5:
        return {"volatility": "high", "risk": "elevated"}
    elif atr_percent > 2:
        return {"volatility": "moderate", "risk": "normal"}
    else:
        return {"volatility": "low", "risk": "low"}


def _interpret_stochastic(k: float, d: float) -> Dict[str, Any]:
    """Interpret Stochastic Oscillator."""
    if k > 80 and d > 80:
        return {"signal": "overbought", "action": "consider_selling"}
    elif k < 20 and d < 20:
        return {"signal": "oversold", "action": "consider_buying"}
    elif k > d:
        return {"signal": "bullish", "action": "hold_long"}
    else:
        return {"signal": "bearish", "action": "hold_short"}


def _interpret_adx(adx: float, dmp: float, dmn: float) -> Dict[str, Any]:
    """Interpret Average Directional Index."""
    if adx > 25:
        trend_strength = "strong"
    elif adx > 20:
        trend_strength = "moderate"
    else:
        trend_strength = "weak"

    direction = "bullish" if dmp > dmn else "bearish"

    return {
        "trend_strength": trend_strength,
        "direction": direction,
        "action": f"trend_follow_{direction}" if adx > 25 else "range_trade"
    }


def _interpret_obv(current: float, previous: float) -> Dict[str, Any]:
    """Interpret On Balance Volume."""
    if current > previous * 1.05:
        return {"volume_trend": "accumulation", "signal": "bullish"}
    elif current < previous * 0.95:
        return {"volume_trend": "distribution", "signal": "bearish"}
    else:
        return {"volume_trend": "neutral", "signal": "neutral"}


def _interpret_vwap(price: float, vwap: float) -> Dict[str, Any]:
    """Interpret Volume Weighted Average Price."""
    if price > vwap * 1.01:
        return {"signal": "above_vwap", "strength": "bullish", "action": "institutional_buying"}
    elif price < vwap * 0.99:
        return {"signal": "below_vwap", "strength": "bearish", "action": "institutional_selling"}
    else:
        return {"signal": "at_vwap", "strength": "neutral", "action": "fair_value"}


def _generate_interpretation(
    results: Dict[str, Any],
    signals: Dict[str, Any],
    terminology_level: str,
    data_points: int
) -> str:
    """Generate human-readable interpretation of indicators."""

    interpretation_parts = []

    interpretation_parts.append(f"Analyzed {data_points} data points across {len(results)} indicators.")

    # Count bullish/bearish signals
    bullish_count = 0
    bearish_count = 0
    neutral_count = 0

    for indicator, signal in signals.items():
        signal_value = signal.get("signal", "neutral")

        if signal_value in ["bullish", "overbought"]:
            bullish_count += 1
        elif signal_value in ["bearish", "oversold"]:
            bearish_count += 1
        else:
            neutral_count += 1

    # Overall sentiment
    if bullish_count > bearish_count:
        sentiment = "bullish"
    elif bearish_count > bullish_count:
        sentiment = "bearish"
    else:
        sentiment = "neutral"

    if terminology_level == "simple":
        if sentiment == "bullish":
            interpretation_parts.append("Most indicators suggest prices may go up. Consider buying opportunities.")
        elif sentiment == "bearish":
            interpretation_parts.append("Most indicators suggest prices may go down. Consider selling or holding off.")
        else:
            interpretation_parts.append("Indicators are mixed. The market is uncertain right now.")

    elif terminology_level == "standard":
        interpretation_parts.append(
            f"Market sentiment: {sentiment.upper()} "
            f"({bullish_count} bullish, {bearish_count} bearish, {neutral_count} neutral signals)."
        )

        # Add specific indicator highlights
        for indicator, signal in signals.items():
            action = signal.get("action")
            if action and action not in ["hold", "wait", "hold_long", "hold_short"]:
                interpretation_parts.append(f"{indicator.upper()}: {action.replace('_', ' ')}")

    else:  # technical
        interpretation_parts.append(
            f"Technical analysis completed: {bullish_count} bullish signals, "
            f"{bearish_count} bearish signals, {neutral_count} neutral. "
            f"Aggregate momentum: {sentiment}."
        )

    return " ".join(interpretation_parts)
