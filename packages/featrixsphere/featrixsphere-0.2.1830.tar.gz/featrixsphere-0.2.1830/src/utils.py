import math
from datetime import datetime


class NodeUpgradingException(Exception):
    """Exception raised when a node is currently upgrading and cannot accept training requests."""
    pass

def convert_to_iso(timestamp: datetime | None) -> str | None:
    if timestamp is None:
        return None

    return timestamp.isoformat()


def convert_from_iso(timestamp: str | None) -> datetime | None:
    if timestamp is None:
        return None

    return datetime.fromisoformat(timestamp)


def clean_numpy_values(data):
    """
    Recursively clean NaN, Inf, and other non-JSON-serializable values from data.
    Converts them to None which is JSON serializable.
    
    Args:
        data: Data structure to clean (dict, list, or primitive)
        
    Returns:
        Cleaned data structure
    """
    import numpy as np

    if isinstance(data, dict):
        return {k: clean_numpy_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_numpy_values(v) for v in data]
    elif isinstance(data, (float, np.floating)):
        if math.isnan(data) or math.isinf(data):
            return None
        return float(data)  # Convert numpy floats to Python floats
    elif isinstance(data, (int, np.integer)):
        return int(data)  # Convert numpy ints to Python ints
    elif isinstance(data, (bool, np.bool_)):
        return bool(data)  # Convert numpy bools to Python bools
    elif isinstance(data, np.ndarray):
        return clean_numpy_values(data.tolist())  # Convert arrays to lists
    elif data is None or isinstance(data, (str, bool)):
        return data
    else:
        # Handle other numpy types or unknown types
        try:
            # Try to convert to a basic Python type
            if hasattr(data, 'item'):  # numpy scalar
                value = data.item()
                if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                    return None
                return value
            else:
                return data
        except:
            # If all else fails, convert to string
            return str(data)
