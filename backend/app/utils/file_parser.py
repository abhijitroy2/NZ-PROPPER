import pandas as pd
import io
from typing import List, Dict, Any
from ..models import PropertyInput


def parse_file(file_content: bytes, filename: str) -> List[Dict[str, Any]]:
    """
    Parse CSV or Excel file and return list of dictionaries.
    Hardcoded column headers matching the expected CSV structure.
    """
    # Expected column names (hardcoded)
    expected_columns = [
        "Date (GMT)",
        "Job Link",
        "Origin URL",
        "Auckland Property Listings Limit",
        "Position",
        "Open Home Status",
        "Agent Name",
        "Agency Name",
        "Listing Date",
        "Property Title",
        "Property Address",
        "Bedrooms",
        "Bathrooms",
        "Area",
        "Price",
        "Property Link"
    ]
    
    try:
        # Determine file type and parse
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_content))
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            raise ValueError(f"Unsupported file type: {filename}")
        
        # Normalize column names (strip whitespace, handle case)
        df.columns = df.columns.str.strip()
        
        # Check for required columns
        missing_columns = []
        for col in expected_columns:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            # Log warning but continue - we'll handle missing columns gracefully
            print(f"Warning: Missing columns: {missing_columns}")
        
        # Fill missing columns with None
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None
        
        # Select only expected columns and fill NaN with None
        df = df[expected_columns].fillna("")
        
        # Convert to list of dictionaries
        properties = df.to_dict('records')
        
        return properties
    
    except Exception as e:
        raise ValueError(f"Error parsing file: {str(e)}")

