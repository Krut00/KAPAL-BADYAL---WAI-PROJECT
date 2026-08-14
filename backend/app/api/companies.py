from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.models import CompanyBasic
from app.services.screener import screener_service
import json

router = APIRouter()

@router.get("/search")
async def search_companies(q: str = Query(..., min_length=1)):
    """Search for companies by name or BSE code"""
    try:
        results = await screener_service.search_company(q)
        return {
            "status": "success",
            "query": q,
            "results": results[:10]  # Limit to 10 results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{bse_code}")
async def get_company_details(bse_code: str):
    """Get company details by BSE code"""
    try:
        if not bse_code.strip():
            raise HTTPException(status_code=400, detail="BSE code is required")
        
        company_data = await screener_service.get_company_data(bse_code)
        
        if not company_data:
            raise HTTPException(status_code=404, detail=f"Company not found: {bse_code}")
        
        return {
            "status": "success",
            "data": company_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{bse_code}/financials")
async def get_company_financials(bse_code: str):
    """Get financial data for a company"""
    try:
        financials = await screener_service.get_historical_financials(bse_code)
        return {
            "status": "success",
            "bse_code": bse_code,
            "financials": financials
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
