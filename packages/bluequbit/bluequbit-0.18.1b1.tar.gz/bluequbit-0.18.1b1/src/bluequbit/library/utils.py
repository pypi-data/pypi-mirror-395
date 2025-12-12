from __future__ import annotations

import numpy as np


def format_floats_for_display(
    obj: dict | list | float | np.floating, decimal_places: int = 2
) -> dict | list | str:
    """
    Recursively format floats in a data structure to scientific notation with specified decimal places

    Parameters:
        obj: The object to format (dict, list, float, etc.)
        decimal_places (int): Number of decimal places in scientific notation (default: 2)

    Returns:
        Formatted object with floats converted to scientific notation strings
    """
    if isinstance(obj, dict):
        return {k: format_floats_for_display(v, decimal_places) for k, v in obj.items()}
    if isinstance(obj, list):
        return [format_floats_for_display(item, decimal_places) for item in obj]
    if isinstance(obj, float):
        return f"{obj:.{decimal_places}e}"
    if isinstance(obj, np.floating):
        return f"{float(obj):.{decimal_places}e}"
    return obj
