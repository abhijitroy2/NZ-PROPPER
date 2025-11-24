from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import io

from .models import ProcessResponse, CalculationResult
from .utils.file_parser import parse_file
from .utils.duplicate_handler import remove_duplicates
from .calculator import FlipCalculator

app = FastAPI(title="NZ PROPPER - Property Flip Calculator", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "NZ PROPPER API"}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and parse CSV/Excel file.
    Returns parsed properties data.
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Parse file
        properties = parse_file(contents, file.filename)
        
        return {
            "success": True,
            "filename": file.filename,
            "properties_count": len(properties),
            "properties": properties[:10]  # Return first 10 for preview
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/calculate")
async def calculate_properties(file: UploadFile = File(...)):
    """
    Process uploaded file, remove duplicates, and calculate flip values.
    Returns results with all calculations.
    """
    try:
        # Read and parse file
        contents = await file.read()
        properties = parse_file(contents, file.filename)
        
        # Remove duplicates
        deduplicated, duplicates_removed = remove_duplicates(properties)
        
        # Calculate for each property
        results: List[CalculationResult] = []
        for prop in deduplicated:
            result = FlipCalculator.calculate(prop)
            results.append(result)
        
        # Calculate summary stats
        good_deals_count = sum(1 for r in results if r.is_good_deal)
        stress_sales_count = sum(1 for r in results if r.has_stress_keywords)
        
        response = ProcessResponse(
            results=results,
            total_properties=len(results),
            good_deals_count=good_deals_count,
            stress_sales_count=stress_sales_count,
            duplicates_removed=duplicates_removed
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


