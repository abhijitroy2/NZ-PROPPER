from typing import List, Dict, Any
from datetime import datetime


def remove_duplicates(properties: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], int]:
    """
    Remove duplicates by Property Address, keeping only the latest entry by Date (GMT).
    
    Args:
        properties: List of property dictionaries
        
    Returns:
        Tuple of (deduplicated list, count of duplicates removed)
    """
    if not properties:
        return [], 0
    
    # Group by Property Address (case-insensitive, trimmed)
    address_groups: Dict[str, List[Dict[str, Any]]] = {}
    
    for prop in properties:
        address = prop.get("Property Address", "").strip().lower()
        if not address:
            # If no address, keep as-is (can't group)
            address = f"_no_address_{len(address_groups)}"
        
        if address not in address_groups:
            address_groups[address] = []
        address_groups[address].append(prop)
    
    # For each group, keep only the latest entry by Date (GMT)
    deduplicated = []
    duplicates_removed = 0
    
    for address, group in address_groups.items():
        if len(group) == 1:
            deduplicated.append(group[0])
        else:
            # Sort by date, keep latest
            sorted_group = sorted(
                group,
                key=lambda x: parse_date(x.get("Date (GMT)", "")),
                reverse=True
            )
            deduplicated.append(sorted_group[0])
            duplicates_removed += len(sorted_group) - 1
    
    return deduplicated, duplicates_removed


def parse_date(date_str: str) -> datetime:
    """
    Parse date string in format "DD/MM/YYYY HH:MM" or "DD/MM/YYYY".
    Returns datetime object, or datetime.min if parsing fails.
    """
    if not date_str or not isinstance(date_str, str):
        return datetime.min
    
    date_str = date_str.strip()
    
    # Try format: DD/MM/YYYY HH:MM
    try:
        return datetime.strptime(date_str, "%d/%m/%Y %H:%M")
    except ValueError:
        pass
    
    # Try format: DD/MM/YYYY
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        pass
    
    # If all parsing fails, return min datetime (will be sorted first)
    return datetime.min


