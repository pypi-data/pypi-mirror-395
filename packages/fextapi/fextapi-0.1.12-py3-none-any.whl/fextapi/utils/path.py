"""Path conversion utilities for fextapi."""

import re
from pathlib import Path


def folder_to_path_param(folder_name: str) -> str:
    """
    Convert folder name with dynamic parameter syntax to FastAPI path parameter.
    
    Examples:
        [productid] -> {productid}
        [userid] -> {userid}
        products -> products (no change)
    
    Args:
        folder_name: The folder name to convert
        
    Returns:
        Converted path parameter string
    """
    # Match [param_name] pattern
    match = re.match(r'^\[(.+)\]$', folder_name)
    if match:
        param_name = match.group(1)
        return f"{{{param_name}}}"
    return folder_name


def build_api_path(relative_path: Path, app_root: Path) -> str:
    """
    Build API path from file system path.
    
    Args:
        relative_path: Path relative to app root (e.g., app/products/[productid])
        app_root: The app root directory (e.g., app/)
        
    Returns:
        API path string (e.g., /products/{productid})
    """
    # Get path relative to app root
    try:
        rel_path = relative_path.relative_to(app_root)
    except ValueError:
        rel_path = relative_path
    
    # Convert each part
    parts = []
    for part in rel_path.parts:
        if part == "route.py":
            continue
        parts.append(folder_to_path_param(part))
    
    # Build path
    if not parts:
        return ""  # Return empty string for root path (FastAPI prefix requirement)
    
    path = "/" + "/".join(parts)
    return path


def extract_path_params(api_path: str) -> list[str]:
    """
    Extract path parameter names from an API path.
    
    Args:
        api_path: API path string (e.g., /products/{productid}/orders/{orderid})
        
    Returns:
        List of parameter names (e.g., ['productid', 'orderid'])
    """
    matches = re.findall(r'\{(.+?)\}', api_path)
    return matches
