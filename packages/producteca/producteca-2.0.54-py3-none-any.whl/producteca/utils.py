"""
Utility functions for the producteca package
"""
from typing import Any, Dict, List, Union
from pydantic import BaseModel


def exclude_empty_values(obj: Any) -> Any:
    """Recursively remove None, empty lists, empty strings, and empty dicts
    
    Note: Preserves 0 values for numeric fields as they are valid prices/quantities
    """
    if isinstance(obj, dict):
        filtered_dict = {}
        for k, v in obj.items():
            # Skip None, empty lists, empty strings, empty dicts
            if v is None or v == [] or v == "" or v == {}:
                continue
            # Keep numeric 0 values - they are valid for prices, quantities, etc.
            filtered_dict[k] = exclude_empty_values(v)
        return filtered_dict
    elif isinstance(obj, list):
        filtered_list = [exclude_empty_values(item) for item in obj if item is not None]
        return [item for item in filtered_list if item != [] and item != "" and item != {}]
    else:
        return obj


def clean_model_dump(model: BaseModel, by_alias: bool = True, exclude_none: bool = True, **kwargs) -> Dict[str, Any]:
    """
    Enhanced model_dump that automatically cleans empty values
    
    Args:
        model: Pydantic model instance
        by_alias: Use field aliases in output
        exclude_none: Exclude None values
        **kwargs: Additional arguments to pass to model_dump
    
    Returns:
        Clean dictionary with empty values removed
    """
    raw_data = model.model_dump(by_alias=by_alias, exclude_none=exclude_none, **kwargs)
    return exclude_empty_values(raw_data)