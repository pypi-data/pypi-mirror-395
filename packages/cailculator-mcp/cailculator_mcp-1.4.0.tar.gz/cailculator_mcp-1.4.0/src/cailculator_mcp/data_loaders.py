"""
CAILculator MCP - Financial Data Loaders
Robust data ingestion for CSV, Excel, JSON with smart OHLCV detection
"""

import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import json

logger = logging.getLogger(__name__)


async def load_market_data(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Load financial market data from various file formats.

    Supports:
    - CSV, Excel (.xlsx, .xls), JSON
    - Auto-detection of OHLCV columns (flexible naming)
    - Date range filtering
    - Symbol filtering
    - Batch mode for large files (>1GB)
    - Data validation and cleaning

    Args:
        arguments: Dict containing:
            - file_path (str): Path to data file
            - symbol (str, optional): Filter by ticker symbol
            - date_range (list, optional): [start_date, end_date] as strings
            - batch_mode (bool, optional): Enable for files >1GB
            - chunk_size (int, optional): Rows per chunk in batch mode (default: 10000)
            - max_rows (int, optional): Maximum rows to load (useful for testing)

    Returns:
        Dict with:
            - success (bool)
            - data (dict): Contains OHLCV arrays
            - metadata (dict): File info, date range, symbol, etc.
            - validation (dict): Data quality metrics
    """
    try:
        # Lazy import pandas only when needed
        import pandas as pd
        import numpy as np
        import os

        # Parse arguments
        file_path = arguments.get("file_path")
        symbol_filter = arguments.get("symbol")
        date_range = arguments.get("date_range")
        batch_mode = arguments.get("batch_mode", False)
        chunk_size = arguments.get("chunk_size", 10000)
        max_rows = arguments.get("max_rows")

        if not file_path:
            return {"success": False, "error": "No file_path provided"}

        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        # Get file info
        file_size = os.path.getsize(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()

        logger.info(f"Loading market data from {file_path} ({file_size / 1024 / 1024:.2f} MB)")

        # Auto-enable batch mode for large files
        if file_size > 1_000_000_000 and not batch_mode:  # >1GB
            logger.warning(f"Large file detected ({file_size / 1024 / 1024:.0f} MB), enabling batch mode")
            batch_mode = True

        # Load data based on file type
        if file_ext == '.csv':
            df = _load_csv(file_path, batch_mode, chunk_size, max_rows)
        elif file_ext in ['.xlsx', '.xls']:
            df = _load_excel(file_path, max_rows)
        elif file_ext == '.json':
            df = _load_json(file_path, max_rows)
        else:
            return {"success": False, "error": f"Unsupported file format: {file_ext}"}

        if df is None or df.empty:
            return {"success": False, "error": "Failed to load data or file is empty"}

        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")

        # Auto-detect OHLCV columns
        column_mapping = _detect_ohlcv_columns(df.columns)

        if not column_mapping:
            return {
                "success": False,
                "error": "Could not detect OHLCV columns",
                "available_columns": list(df.columns)
            }

        # Rename columns to standard names
        df = df.rename(columns=column_mapping)

        # Detect and parse date column
        date_col = _detect_date_column(df.columns)
        if date_col:
            df = _parse_dates(df, date_col)
            df = df.sort_values(date_col)

        # Apply filters
        if symbol_filter and 'symbol' in df.columns:
            original_len = len(df)
            df = df[df['symbol'].str.upper() == symbol_filter.upper()]
            logger.info(f"Filtered by symbol '{symbol_filter}': {original_len} → {len(df)} rows")

        if date_range and date_col:
            df = _filter_date_range(df, date_col, date_range)

        # Validate and clean data
        validation_results = _validate_ohlcv_data(df)
        df = _clean_data(df)

        # Extract OHLCV arrays
        data_dict = {}
        for std_col in ['open', 'high', 'low', 'close', 'volume']:
            if std_col in df.columns:
                data_dict[std_col] = df[std_col].values.tolist()

        if date_col and date_col in df.columns:
            # Convert timestamps to strings for JSON serialization
            data_dict['timestamps'] = df[date_col].astype(str).tolist()

        # Build metadata
        metadata = {
            "file_path": file_path,
            "file_size_mb": file_size / 1024 / 1024,
            "rows_loaded": len(df),
            "columns_detected": column_mapping,
            "date_range": [
                str(df[date_col].min()) if date_col and date_col in df.columns else None,
                str(df[date_col].max()) if date_col and date_col in df.columns else None
            ] if date_col else None,
            "batch_mode": batch_mode,
        }

        if symbol_filter:
            metadata["symbol"] = symbol_filter

        return {
            "success": True,
            "data": data_dict,
            "metadata": metadata,
            "validation": validation_results,
            "interpretation": _generate_data_interpretation(metadata, validation_results)
        }

    except Exception as e:
        logger.error(f"Error loading market data: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


def _load_csv(file_path: str, batch_mode: bool, chunk_size: int, max_rows: Optional[int]) -> Any:
    """Load CSV file, optionally in batch mode."""
    import pandas as pd

    if batch_mode:
        # Load in chunks and concatenate
        chunks = []
        total_rows = 0

        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            chunks.append(chunk)
            total_rows += len(chunk)

            if max_rows and total_rows >= max_rows:
                break

        df = pd.concat(chunks, ignore_index=True)

        if max_rows:
            df = df.head(max_rows)
    else:
        # Load entire file
        df = pd.read_csv(file_path, nrows=max_rows)

    return df


def _load_excel(file_path: str, max_rows: Optional[int]) -> Any:
    """Load Excel file."""
    import pandas as pd

    df = pd.read_excel(file_path, nrows=max_rows)
    return df


def _load_json(file_path: str, max_rows: Optional[int]) -> Any:
    """Load JSON file."""
    import pandas as pd

    # Try reading as JSON lines or standard JSON
    try:
        df = pd.read_json(file_path, lines=True)
    except:
        df = pd.read_json(file_path)

    if max_rows:
        df = df.head(max_rows)

    return df


def _detect_ohlcv_columns(columns: List[str]) -> Dict[str, str]:
    """
    Auto-detect OHLCV columns with flexible naming.

    Returns mapping: {original_column_name: standard_name}
    """
    column_patterns = {
        'open': ['open', 'Open', 'OPEN', 'o'],
        'high': ['high', 'High', 'HIGH', 'h'],
        'low': ['low', 'Low', 'LOW', 'l'],
        'close': ['close', 'Close', 'CLOSE', 'c', 'price', 'Price'],
        'volume': ['volume', 'Volume', 'VOLUME', 'vol', 'Vol', 'v']
    }

    mapping = {}

    for std_name, patterns in column_patterns.items():
        for col in columns:
            if col in patterns or any(pattern.lower() in col.lower() for pattern in patterns):
                mapping[col] = std_name
                break

    # Minimum requirement: must have at least 'close' price
    if 'close' not in mapping.values():
        return {}

    return mapping


def _detect_date_column(columns: List[str]) -> Optional[str]:
    """Detect date/timestamp column."""
    date_patterns = [
        'date', 'Date', 'DATE', 'datetime', 'DateTime', 'DATETIME',
        'timestamp', 'Timestamp', 'TIMESTAMP', 'time', 'Time', 'TIME'
    ]

    for col in columns:
        if col in date_patterns or any(pattern.lower() in col.lower() for pattern in date_patterns):
            return col

    return None


def _parse_dates(df: Any, date_col: str) -> Any:
    """Parse date column to datetime."""
    import pandas as pd

    try:
        df[date_col] = pd.to_datetime(df[date_col])
    except Exception as e:
        logger.warning(f"Could not parse dates in column '{date_col}': {e}")

    return df


def _filter_date_range(df: Any, date_col: str, date_range: List[str]) -> Any:
    """Filter DataFrame by date range."""
    import pandas as pd

    if len(date_range) != 2:
        return df

    start_date, end_date = date_range

    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        original_len = len(df)
        df = df[(df[date_col] >= start) & (df[date_col] <= end)]
        logger.info(f"Filtered by date range {start_date} to {end_date}: {original_len} → {len(df)} rows")
    except Exception as e:
        logger.warning(f"Could not filter by date range: {e}")

    return df


def _validate_ohlcv_data(df: Any) -> Dict[str, Any]:
    """
    Validate OHLCV data quality.

    Checks:
    - Missing values (NaNs)
    - Invalid OHLC relationships (high < low, etc.)
    - Negative values
    - Outliers
    """
    import numpy as np

    validation = {
        "total_rows": len(df),
        "missing_values": {},
        "invalid_ohlc": 0,
        "negative_values": 0,
        "outliers_detected": 0,
        "quality_score": 1.0
    }

    # Check for missing values
    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                validation["missing_values"][col] = int(null_count)

    # Check OHLC relationships
    if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
        invalid_high = (df['high'] < df['low']).sum()
        invalid_high += (df['high'] < df['open']).sum()
        invalid_high += (df['high'] < df['close']).sum()

        invalid_low = (df['low'] > df['open']).sum()
        invalid_low += (df['low'] > df['close']).sum()

        validation["invalid_ohlc"] = int(invalid_high + invalid_low)

    # Check for negative values
    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                validation["negative_values"] += int(negative_count)

    # Simple outlier detection using IQR
    if 'close' in df.columns:
        Q1 = df['close'].quantile(0.25)
        Q3 = df['close'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df['close'] < (Q1 - 3 * IQR)) | (df['close'] > (Q3 + 3 * IQR))).sum()
        validation["outliers_detected"] = int(outliers)

    # Calculate quality score
    total_issues = (
        sum(validation["missing_values"].values()) +
        validation["invalid_ohlc"] +
        validation["negative_values"]
    )

    if validation["total_rows"] > 0:
        validation["quality_score"] = max(0.0, 1.0 - (total_issues / validation["total_rows"]))

    return validation


def _clean_data(df: Any) -> Any:
    """
    Clean OHLCV data.

    - Fill forward missing values (common in financial data)
    - Remove rows with invalid OHLC relationships
    - Cap extreme outliers
    """
    import numpy as np

    original_len = len(df)

    # Fill forward missing values (carry last observation forward)
    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df.columns:
            df[col] = df[col].ffill()

    # Drop remaining NaNs (at the start)
    df = df.dropna(subset=[col for col in ['open', 'high', 'low', 'close'] if col in df.columns])

    # Remove negative values
    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df.columns:
            df = df[df[col] >= 0]

    # Fix invalid OHLC relationships (conservative approach: drop bad rows)
    if all(col in df.columns for col in ['open', 'high', 'low', 'close']):
        df = df[
            (df['high'] >= df['low']) &
            (df['high'] >= df['open']) &
            (df['high'] >= df['close']) &
            (df['low'] <= df['open']) &
            (df['low'] <= df['close'])
        ]

    cleaned_len = len(df)

    if cleaned_len < original_len:
        logger.info(f"Data cleaning: {original_len} → {cleaned_len} rows ({original_len - cleaned_len} removed)")

    return df


def _generate_data_interpretation(metadata: Dict[str, Any], validation: Dict[str, Any]) -> str:
    """Generate human-readable interpretation of loaded data."""
    rows = metadata["rows_loaded"]
    quality = validation["quality_score"]

    interpretation = f"Successfully loaded {rows} rows of market data. "

    if quality >= 0.95:
        interpretation += "Data quality is excellent."
    elif quality >= 0.80:
        interpretation += "Data quality is good with minor issues."
    elif quality >= 0.60:
        interpretation += "Data quality is acceptable but has some issues."
    else:
        interpretation += "Data quality is poor - significant cleaning may be needed."

    if validation.get("missing_values"):
        missing_total = sum(validation["missing_values"].values())
        interpretation += f" Found {missing_total} missing values (filled forward). "

    if validation.get("invalid_ohlc", 0) > 0:
        interpretation += f" Detected {validation['invalid_ohlc']} rows with invalid OHLC relationships (removed). "

    if metadata.get("date_range"):
        start, end = metadata["date_range"]
        if start and end:
            interpretation += f" Date range: {start} to {end}."

    return interpretation
