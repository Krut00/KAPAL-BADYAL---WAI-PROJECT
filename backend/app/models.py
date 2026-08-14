# Data models for the CCC Analyzer

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CompanyBasic(BaseModel):
    """Basic company information"""
    bse_code: str
    company_name: str
    sector: str
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None

class FinancialMetric(BaseModel):
    """Financial metric for a specific period"""
    period: str
    value: float
    date: Optional[str] = None

class CCCComponents(BaseModel):
    """CCC components breakdown"""
    inventory_days: float
    receivable_days: float
    payable_days: float
    ccc: float
    period: str

class CompanyAnalysis(BaseModel):
    """Complete company analysis"""
    company_name: str
    bse_code: str
    sector: str
    current_ccc: CCCComponents
    historical_ccc: List[CCCComponents]
    profitability_data: Dict[str, Any]
    working_capital_analysis: Dict[str, Any]
    problem_identification: Dict[str, Any]

class ComparisonResult(BaseModel):
    """Comparison of two companies"""
    company_1: CompanyAnalysis
    company_2: CompanyAnalysis
    comparison_metrics: Dict[str, Any]
    insights: List[str]

class CCCTrend(BaseModel):
    """CCC trend over time"""
    period: str
    inventory_days: float
    receivable_days: float
    payable_days: float
    ccc: float
    trend_analysis: Dict[str, Any]
