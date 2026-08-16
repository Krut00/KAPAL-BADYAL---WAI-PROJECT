from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from app.services.ccc_analysis import CCCAnalysisService, WorkingCapitalProblem
from app.services.screener import screener_service
from app.services.data_validator import DataValidator

router = APIRouter()

class CCCInputData(BaseModel):
    """Input data for CCC calculation"""
    average_inventory: float
    cost_of_goods_sold: float
    average_receivables: float
    revenue: float
    average_payables: float

class ComparisonRequest(BaseModel):
    """Request for comparing two companies"""
    company1_bse: str
    company2_bse: str
    sector: Optional[str] = "default"

@router.post("/calculate-ccc")
async def calculate_ccc(data: CCCInputData):
    """Calculate CCC components from financial data"""
    try:
        financial_data = data.dict()
        ccc_components = CCCAnalysisService.calculate_ccc_components(financial_data)
        
        return {
            "status": "success",
            "ccc_components": ccc_components
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-company")
async def analyze_single_company(
    bse_code: str,
    sector: str = "default"
):
    """Analyze a single company's working capital efficiency"""
    try:
        # Fetch company data
        company_data = await screener_service.get_company_data(bse_code)
        if not company_data:
            raise HTTPException(status_code=404, detail=f"Company not found: {bse_code}")
        
        # Use Screener's published operating ratios when available.
        ccc_components = company_data.get('ccc_components') or CCCAnalysisService.calculate_ccc_components(company_data)
        
        # Get the current period from historical data (usually the most recent/latest)
        historical_data = company_data.get('historical', [])
        current_period = historical_data[-1].get('period', '') if historical_data else ''
        
        # Validate and correct data if needed, including current period
        ccc_components = DataValidator.validate_and_correct(bse_code, current_period, ccc_components)
        ccc_components = DataValidator.validate_ccc_calculation(ccc_components)
        
        benchmark = CCCAnalysisService.benchmark_for_industry(company_data.get('industry', ''))
        
        # Identify problems
        problems, assessment = CCCAnalysisService.identify_problems(
            ccc_components, 
            sector=sector,
            available_components=company_data.get('data_quality', {}).get('available_components'),
            benchmark_override=benchmark
        )
        
        # Calculate trends from the same annual records used for the current result.
        historical_ccc = []
        for period in company_data.get('historical', []):
            if 'ccc' in period:
                period_ccc = {
                    'inventory_days': period['inventory_days'],
                    'receivable_days': period['receivable_days'],
                    'payable_days': period['payable_days'],
                    'ccc': period['ccc'],
                }
                # Validate and correct if needed
                period_ccc = DataValidator.validate_and_correct(bse_code, period.get('period', ''), period_ccc)
                period_ccc = DataValidator.validate_ccc_calculation(period_ccc)
            else:
                period_ccc = CCCAnalysisService.calculate_ccc_components({
                    'average_inventory': period['inventory'],
                    'cost_of_goods_sold': period['cost_of_goods_sold'],
                    'average_receivables': period['receivables'],
                    'revenue': period['revenue'],
                    'average_payables': period['payables'],
                })
            historical_ccc.append({**period_ccc, 'period': period['period']})
        trends = CCCAnalysisService.analyze_trend(list(reversed(historical_ccc)))
        investor_insights = CCCAnalysisService.company_insights(company_data.get('historical', []), ccc_components)
        
        return {
            "status": "success",
            "company": {
                "name": company_data.get('company_name'),
                "bse_code": bse_code,
                "sector": sector
            },
            "ccc_analysis": {
                "current": ccc_components,
                "problems": [
                    {
                        "type": p.problem_type,
                        "severity": p.severity,
                        "description": p.description,
                        "impact": p.impact
                    } for p in problems
                ],
                "assessment": assessment
            },
            "trends": trends,
            "historical_ccc": historical_ccc,
            "data_quality": company_data.get('data_quality', {}),
            "benchmark": benchmark,
            "investor_insights": investor_insights,
            "profitability": company_data.get('profitability_data', {})
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare-companies")
async def compare_two_companies(request: ComparisonRequest):
    """Compare CCC between two companies"""
    try:
        # Fetch data for both companies
        company1_data = await screener_service.get_company_data(request.company1_bse)
        company2_data = await screener_service.get_company_data(request.company2_bse)
        
        if not company1_data or not company2_data:
            raise HTTPException(status_code=404, detail="One or both companies not found")
        
        # Use the same Screener-published ratios as the single-company analysis.
        ccc1 = company1_data.get('ccc_components') or CCCAnalysisService.calculate_ccc_components(company1_data)
        ccc2 = company2_data.get('ccc_components') or CCCAnalysisService.calculate_ccc_components(company2_data)
        benchmark1 = CCCAnalysisService.benchmark_for_industry(company1_data.get('industry', ''))
        benchmark2 = CCCAnalysisService.benchmark_for_industry(company2_data.get('industry', ''))
        
        # Identify problems for both
        problems1, assessment1 = CCCAnalysisService.identify_problems(
            ccc1,
            sector=request.sector,
            available_components=company1_data.get('data_quality', {}).get('available_components'),
            benchmark_override=benchmark1
        )
        problems2, assessment2 = CCCAnalysisService.identify_problems(
            ccc2,
            sector=request.sector,
            available_components=company2_data.get('data_quality', {}).get('available_components'),
            benchmark_override=benchmark2
        )
        
        # Calculate differences
        comparison_metrics = {
            "ccc_difference": round(ccc1['ccc'] - ccc2['ccc'], 2),
            "inventory_difference": round(ccc1['inventory_days'] - ccc2['inventory_days'], 2),
            "receivable_difference": round(ccc1['receivable_days'] - ccc2['receivable_days'], 2),
            "payable_difference": round(ccc1['payable_days'] - ccc2['payable_days'], 2),
        }
        
        insights = CCCAnalysisService.compare_insights(
            company1_data.get('company_name', request.company1_bse),
            company2_data.get('company_name', request.company2_bse),
            ccc1,
            ccc2
        )
        
        return {
            "status": "success",
            "company1": {
                "name": company1_data.get('company_name'),
                "bse_code": request.company1_bse,
                "ccc": ccc1,
                "assessment": assessment1
            },
            "company2": {
                "name": company2_data.get('company_name'),
                "bse_code": request.company2_bse,
                "ccc": ccc2,
                "assessment": assessment2
            },
            "comparison": comparison_metrics,
            "insights": insights
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/project-improvement")
async def project_ccc_improvement(
    current_ccc: Dict[str, float],
    target_improvements: Dict[str, float]
):
    """Project CCC improvement scenarios"""
    try:
        projection = CCCAnalysisService.project_ccc_improvement(current_ccc, target_improvements)
        return {
            "status": "success",
            "projection": projection
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
