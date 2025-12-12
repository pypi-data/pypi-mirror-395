"""
HITL Approval Processing Utilities

Generic utilities for processing approval responses from HITL UIs.
These functions are implementation-agnostic and help with common HITL patterns.

Functions:
- extract_field: Extract a specific field from nested response structure
- filter_fields: Filter out system/metadata fields from user data
- is_approved: Check if approval was approved or rejected
- build_outputs: Build output dictionary with common structure
- validate_approval_response: Validate approval response structure
- merge_input_with_parameters: Merge workflow input with task config

These utilities work with any HITL task structure.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


def extract_field(
    approval_response: Dict[str, Any],
    field_name: str,
    default: Any = None
) -> Any:
    """
    Extract a field from approval response, checking both top-level and nested data.
    
    Handles common nesting patterns in approval responses:
    - Top level: {field_name: value}
    - Nested in data: {"data": {field_name: value}}
    
    Args:
        approval_response: The approval response from the UI
        field_name: Name of the field to extract
        default: Default value if field not found
    
    Returns:
        Field value or default if not found
    
    Example:
        >>> response = {"approved": True, "user_name": "John"}
        >>> name = extract_field(response, "user_name")
        >>> print(name)  # "John"
        
        >>> response = {"data": {"user_name": "John"}}
        >>> name = extract_field(response, "user_name")
        >>> print(name)  # "John"
    """
    # Try top-level first
    if field_name in approval_response:
        return approval_response[field_name]
    
    # Try nested in data
    nested_data = approval_response.get("data", {})
    if isinstance(nested_data, dict) and field_name in nested_data:
        return nested_data[field_name]
    
    return default


def filter_fields(
    data: Dict[str, Any],
    exclude_fields: Optional[List[str]] = None,
    include_only: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Filter fields from a dictionary based on exclude or include lists.
    
    Useful for removing system/metadata fields or extracting only specific fields.
    
    Args:
        data: Source dictionary to filter
        exclude_fields: List of field names to exclude (ignored if include_only is set)
        include_only: List of field names to include (takes precedence over exclude_fields)
    
    Returns:
        Filtered dictionary
    
    Example:
        >>> data = {"name": "John", "age": 30, "_metadata": {}, "approved": True}
        >>> filtered = filter_fields(data, exclude_fields=["_metadata", "approved"])
        >>> print(filtered)  # {"name": "John", "age": 30}
        
        >>> filtered = filter_fields(data, include_only=["name", "age"])
        >>> print(filtered)  # {"name": "John", "age": 30}
    """
    if include_only:
        return {k: v for k, v in data.items() if k in include_only}
    
    if exclude_fields:
        exclude_set = set(exclude_fields)
        return {k: v for k, v in data.items() if k not in exclude_set}
    
    return data.copy()


def is_approved(approval_response: Dict[str, Any]) -> bool:
    """
    Check if the approval was approved or rejected.
    
    Checks multiple possible fields for approval status:
    - approved: boolean field
    - decision: "approved"/"rejected" string
    
    Args:
        approval_response: The approval response from the UI
    
    Returns:
        True if approved, False if rejected
    
    Example:
        >>> response = {"approved": True, "comments": "Looks good"}
        >>> is_approved(response)  # True
        
        >>> response = {"decision": "rejected"}
        >>> is_approved(response)  # False
    """
    # Check boolean approved field
    if "approved" in approval_response:
        return bool(approval_response["approved"])
    
    # Check decision field
    if "decision" in approval_response:
        decision = approval_response["decision"]
        return decision == "approved" or decision is True
    
    # Default to approved if not specified
    return True


def build_outputs(
    approval_response: Dict[str, Any],
    include_timestamp: bool = True,
    additional_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Build output dictionary from approval response with common metadata.
    
    This is a minimal helper that adds standard metadata fields.
    Customize the output structure based on your task's needs.
    
    Args:
        approval_response: The approval response from the UI
        include_timestamp: Whether to include processed_at timestamp
        additional_metadata: Additional metadata fields to include
    
    Returns:
        Dictionary with approval response and optional metadata
    
    Example:
        >>> response = {"approved": True, "data": {"name": "John"}}
        >>> outputs = build_outputs(response)
        >>> print(outputs["approved"])  # True
        >>> print(outputs["processed_at"])  # "2025-12-06T..."
    
    Note:
        This is a minimal helper. For task-specific output structure,
        implement your own output builder that extracts and formats
        the specific fields your workflow needs.
    """
    outputs = approval_response.copy()
    
    if include_timestamp:
        outputs["processed_at"] = datetime.utcnow().isoformat()
    
    if additional_metadata:
        if "metadata" not in outputs:
            outputs["metadata"] = {}
        outputs["metadata"].update(additional_metadata)
    
    return outputs


def validate_approval_response(
    approval_response: Dict[str, Any]
) -> Tuple[bool, str]:
    """
    Validate that the approval response has required structure.
    
    Performs basic validation to ensure the response is properly formatted.
    
    Args:
        approval_response: The approval response to validate
    
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if valid, False otherwise
        - error_message: Empty if valid, error description if invalid
    
    Example:
        >>> response = {"approved": True}
        >>> is_valid, error = validate_approval_response(response)
        >>> print(is_valid)  # True
        
        >>> response = "not a dict"
        >>> is_valid, error = validate_approval_response(response)
        >>> print(is_valid)  # False
        >>> print(error)  # "Approval response must be a dictionary"
    """
    if not isinstance(approval_response, dict):
        return False, "Approval response must be a dictionary"
    
    # Additional validation can be added here
    # For example, check for required fields, data types, etc.
    
    return True, ""


def merge_input_with_parameters(
    input_data: Dict[str, Any],
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge input_data and parameters into a single dictionary.
    
    Parameters take precedence over input_data for overlapping keys.
    This is useful for combining workflow input with task configuration.
    
    Args:
        input_data: Data from previous workflow tasks
        parameters: Task configuration parameters
    
    Returns:
        Merged dictionary with parameters taking precedence
    
    Example:
        >>> input_data = {"name": "John", "age": 30}
        >>> parameters = {"age": 31, "title": "Review User"}
        >>> merged = merge_input_with_parameters(input_data, parameters)
        >>> print(merged)  # {"name": "John", "age": 31, "title": "Review User"}
    """
    return {**input_data, **parameters}
