"""
Utility functions shared between sync and async clients.
"""

import re
from typing import Union

from blocky.exceptions import BlockyValidationError


def validate_decimal(
    decimal_str: str = None,
    precision: int = 8,
    min_value: str = '-99999999.99999999',
    max_value: str = '99999999.99999999'
) -> str:
    """
    Validate and normalize a decimal string value.
    
    Args:
        decimal_str: The decimal string to validate.
        precision: Maximum number of decimal places allowed.
        min_value: Minimum allowed value.
        max_value: Maximum allowed value.
        
    Returns:
        Normalized decimal string.
        
    Raises:
        BlockyValidationError: If validation fails.
    """
    if not decimal_str:
        raise BlockyValidationError("Decimal value is empty.")
    
    # Handle leading/trailing dots (e.g., '.5' -> '0.5', '5.' -> '5.0')
    if decimal_str.startswith('.'):
        decimal_str = '0' + decimal_str
    if decimal_str.endswith('.'):
        decimal_str = decimal_str + '0'
    
    # Regex to validate precision
    regex_pattern = rf'^-?\d{{1,8}}(\.\d{{1,{precision}}})?$'
    if not re.match(regex_pattern, decimal_str):
        raise BlockyValidationError(f"Invalid decimal format: {decimal_str}")
    
    decimal_value = float(decimal_str)
    if not (float(min_value) <= decimal_value <= float(max_value)):
        raise BlockyValidationError(
            f"Decimal value must be between {min_value} and {max_value}, "
            f"provided: {decimal_value}"
        )
    
    return str(decimal_value)


def parse_timeframe_ns(timeframe: Union[int, str]) -> int:
    """
    Parse a timeframe string to nanoseconds.
    
    Args:
        timeframe: Either nanoseconds as int, or a string like '1m', '1H', '1D'.
        
    Returns:
        Timeframe in nanoseconds.
        
    Raises:
        BlockyValidationError: If timeframe format is invalid.
    """
    if isinstance(timeframe, int):
        return timeframe
    
    # Standard timeframe mappings
    time_map = {
        '1m': 60_000_000_000,
        '3m': 180_000_000_000,
        '5m': 300_000_000_000,
        '15m': 900_000_000_000,
        '30m': 1_800_000_000_000,
        '1H': 3_600_000_000_000,
        '2H': 7_200_000_000_000,
        '4H': 14_400_000_000_000,
        '6H': 21_600_000_000_000,
        '8H': 28_800_000_000_000,
        '12H': 43_200_000_000_000,
        '1D': 86_400_000_000_000,
        '3D': 259_200_000_000_000,
        '1W': 604_800_000_000_000,
        '1M': 2_592_000_000_000_000,
    }
    
    if timeframe in time_map:
        return time_map[timeframe]
    
    # Fallback to regex parsing
    match = re.match(r'^(\d+)([mMhHdDwWy])$', timeframe)
    if match:
        num = int(match.group(1))
        unit = match.group(2).lower()
        ns = 1_000_000_000  # 1 second in nanoseconds
        
        if unit == 'm':
            return num * 60 * ns
        elif unit == 'h':
            return num * 3600 * ns
        elif unit == 'd':
            return num * 86400 * ns
        elif unit == 'w':
            return num * 604800 * ns
    
    raise BlockyValidationError(f"Invalid timeframe: {timeframe}")


# Constants
DEFAULT_ENDPOINT = 'https://blocky.com.br/api/v1'
DEFAULT_TIMEOUT = 30.0
MAX_SUB_WALLET_ID = 16384
MAX_INT64 = (1 << 63) - 1
