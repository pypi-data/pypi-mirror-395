"""HR Platform SDK Utilities.

Helper functions for data conversion and integration.

Example:
    >>> from hr_platform.utils import records_to_dataframe
    >>> df = records_to_dataframe(records)
"""

try:
    from hr_platform.utils.pandas_helpers import (
        entity_breakdown_to_dataframe,
        records_to_dataframe,
        trends_to_dataframe,
    )

    __all__ = [
        "records_to_dataframe",
        "trends_to_dataframe",
        "entity_breakdown_to_dataframe",
    ]
except ImportError:
    # pandas not installed
    __all__ = []
