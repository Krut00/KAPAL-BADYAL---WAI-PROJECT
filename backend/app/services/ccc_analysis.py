from typing import Dict, Any, List, Tuple
from datetime import datetime
import numpy as np
from dataclasses import dataclass

@dataclass
class WorkingCapitalProblem:
    """Represents a working capital problem identified"""
    problem_type: str  # "high_inventory", "high_receivables", "low_payables", "increasing_ccc"
    severity: float  # 0-1 scale
    description: str
    impact: str

class CCCAnalysisService:
    """Service for analyzing Cash Conversion Cycle"""
    
    # Benchmarks for different sectors (can be expanded)
    SECTOR_BENCHMARKS = {
        'default': {
            'inventory_days': 60,
            'receivable_days': 30,
            'payable_days': 45,
            'ccc': 45
        },
        'retail': {
            'inventory_days': 40,
            'receivable_days': 10,
            'payable_days': 35,
            'ccc': 15
        },
        'manufacturing': {
            'inventory_days': 90,
            'receivable_days': 45,
            'payable_days': 60,
            'ccc': 75
        },
        'services': {
            'inventory_days': 5,
            'receivable_days': 30,
            'payable_days': 30,
            'ccc': 5
        }
    }

    INDUSTRY_BENCHMARKS = {
        'software': {'inventory_days': 15, 'receivable_days': 75, 'payable_days': 45, 'ccc': 45},
        'it services': {'inventory_days': 15, 'receivable_days': 75, 'payable_days': 45, 'ccc': 45},
        'oil': {'inventory_days': 50, 'receivable_days': 20, 'payable_days': 60, 'ccc': 10},
        'refin': {'inventory_days': 50, 'receivable_days': 20, 'payable_days': 60, 'ccc': 10},
        'retail': {'inventory_days': 60, 'receivable_days': 10, 'payable_days': 45, 'ccc': 25},
        'automobile': {'inventory_days': 60, 'receivable_days': 30, 'payable_days': 60, 'ccc': 30},
        'pharmaceutical': {'inventory_days': 120, 'receivable_days': 75, 'payable_days': 90, 'ccc': 105},
        'manufacturing': {'inventory_days': 90, 'receivable_days': 45, 'payable_days': 60, 'ccc': 75},
    }

    @classmethod
    def benchmark_for_industry(cls, industry: str = '') -> Dict[str, Any]:
        industry_text = (industry or '').lower()
        for keyword, benchmark in cls.INDUSTRY_BENCHMARKS.items():
            if keyword in industry_text:
                return {
                    **benchmark,
                    'industry': industry,
                    'source': 'Industry reference profile based on Screener.in classification and peer operating-ratio practice'
                }
        return {
            **cls.SECTOR_BENCHMARKS['default'],
            'industry': industry or 'Unclassified',
            'source': 'General reference profile used because Screener.in did not provide a mapped industry'
        }
    
    @staticmethod
    def calculate_ccc_components(financial_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate CCC components from financial data
        
        Formulas:
        - Inventory Days = (Average Inventory / COGS) * 365
        - Receivable Days = (Average Receivables / Revenue) * 365
        - Payable Days = (Average Payables / COGS) * 365
        - CCC = Inventory Days + Receivable Days - Payable Days
        """
        try:
            required = (
                'average_inventory', 'cost_of_goods_sold', 'average_receivables',
                'revenue', 'average_payables'
            )
            missing = [name for name in required if financial_data.get(name) is None]
            if missing:
                raise ValueError(f"Missing financial inputs: {', '.join(missing)}")

            inventory = financial_data['average_inventory']
            cogs = financial_data['cost_of_goods_sold']
            receivables = financial_data['average_receivables']
            revenue = financial_data['revenue']
            payables = financial_data['average_payables']

            if cogs <= 0 or revenue <= 0:
                raise ValueError('Revenue and cost of goods sold must be positive')
            
            inventory_days = (inventory / cogs * 365) if cogs > 0 else 0
            receivable_days = (receivables / revenue * 365) if revenue > 0 else 0
            payable_days = (payables / cogs * 365) if cogs > 0 else 0
            ccc = inventory_days + receivable_days - payable_days
            
            return {
                'inventory_days': round(inventory_days, 2),
                'receivable_days': round(receivable_days, 2),
                'payable_days': round(payable_days, 2),
                'ccc': round(ccc, 2)
            }
        except Exception as e:
            print(f"Error calculating CCC components: {e}")
            return {
                'inventory_days': 0,
                'receivable_days': 0,
                'payable_days': 0,
                'ccc': 0
            }
    
    @staticmethod
    def identify_problems(
        current_ccc: Dict[str, float],
        historical_ccc: List[Dict[str, float]] = None,
        sector: str = 'default',
        available_components: Dict[str, bool] = None,
        benchmark_override: Dict[str, Any] = None
    ) -> Tuple[List[WorkingCapitalProblem], str]:
        """
        Identify working capital problems using pattern recognition
        Returns: (list of problems, overall assessment)
        """
        problems = []
        available_components = available_components or {}
        benchmark = benchmark_override or CCCAnalysisService.SECTOR_BENCHMARKS.get(sector, CCCAnalysisService.SECTOR_BENCHMARKS['default'])
        
        # Check for high inventory days
        if available_components.get('inventory_days', True) and current_ccc['inventory_days'] > benchmark['inventory_days'] * 1.3:
            severity = min(1.0, (current_ccc['inventory_days'] - benchmark['inventory_days']) / benchmark['inventory_days'])
            problems.append(WorkingCapitalProblem(
                problem_type='high_inventory',
                severity=severity,
                description=f"Inventory Days at {current_ccc['inventory_days']:.1f} days (benchmark: {benchmark['inventory_days']:.1f})",
                impact="Inventory may be moving slowly, indicating potential overstocking or slow sales"
            ))
        
        # Check for high receivable days
        if current_ccc['receivable_days'] > benchmark['receivable_days'] * 1.3:
            severity = min(1.0, (current_ccc['receivable_days'] - benchmark['receivable_days']) / benchmark['receivable_days'])
            problems.append(WorkingCapitalProblem(
                problem_type='high_receivables',
                severity=severity,
                description=f"Receivable Days at {current_ccc['receivable_days']:.1f} days (benchmark: {benchmark['receivable_days']:.1f})",
                impact="Customers may be taking longer to pay, creating cash flow pressure"
            ))
        
        # Check for low payable days
        if available_components.get('payable_days', True) and current_ccc['payable_days'] < benchmark['payable_days'] * 0.7:
            severity = min(1.0, (benchmark['payable_days'] - current_ccc['payable_days']) / benchmark['payable_days'])
            problems.append(WorkingCapitalProblem(
                problem_type='low_payables',
                severity=severity,
                description=f"Payable Days at {current_ccc['payable_days']:.1f} days (benchmark: {benchmark['payable_days']:.1f})",
                impact="Company may be paying suppliers too quickly, draining cash"
            ))
        
        # Check for increasing CCC trend
        if historical_ccc and len(historical_ccc) > 1:
            recent_ccc = [h['ccc'] for h in historical_ccc[-3:]]
            if len(recent_ccc) >= 2 and recent_ccc[-1] > recent_ccc[0]:
                avg_increase = (recent_ccc[-1] - recent_ccc[0]) / len(recent_ccc)
                severity = min(1.0, avg_increase / benchmark['ccc'])
                problems.append(WorkingCapitalProblem(
                    problem_type='increasing_ccc',
                    severity=severity,
                    description=f"CCC is trending upward: {recent_ccc[-3:]}",
                    impact="More cash is getting locked into the operating cycle over time"
                ))
        
        # Generate overall assessment
        ccc = current_ccc['ccc']
        benchmark_ccc = benchmark['ccc']
        ccc_gap = ccc - benchmark_ccc
        if not problems:
            assessment = (
                f"Working capital appears controlled: the cash conversion cycle is {ccc:.1f} days, "
                f"about {abs(ccc_gap):.1f} days {'above' if ccc_gap >= 0 else 'below'} the reference level. "
                "Continue monitoring collections, inventory turns, and supplier terms because a single period "
                "can be affected by seasonality."
            )
        else:
            focus = ', '.join(problem.problem_type.replace('_', ' ') for problem in problems)
            assessment = (
                f"Working capital needs attention across {len(problems)} area(s): {focus}. "
                f"The cash conversion cycle is {ccc:.1f} days, {abs(ccc_gap):.1f} days "
                f"{'above' if ccc_gap >= 0 else 'below'} the reference level of {benchmark_ccc:.1f} days. "
                "This indicates that operating cash may remain tied up longer than necessary. "
                "Prioritize the highest-severity driver first, then track the result over several reporting periods."
            )
        
        return problems, assessment
    
    @staticmethod
    def analyze_trend(historical_data: List[Dict[str, float]]) -> Dict[str, Any]:
        """Analyze trends in CCC components over time"""
        if not historical_data or len(historical_data) < 2:
            return {}
        
        ccc_values = [d['ccc'] for d in historical_data]
        inventory_values = [d['inventory_days'] for d in historical_data]
        receivable_values = [d['receivable_days'] for d in historical_data]
        payable_values = [d['payable_days'] for d in historical_data]
        
        # Calculate trends
        ccc_trend = ccc_values[-1] - ccc_values[0]
        ccc_avg_change = np.mean(np.diff(ccc_values))
        
        return {
            'ccc_trend': 'improving' if ccc_trend < 0 else 'deteriorating' if ccc_trend > 0 else 'stable',
            'ccc_total_change': round(ccc_trend, 2),
            'ccc_avg_change_per_period': round(ccc_avg_change, 2),
            'inventory_trend': round(inventory_values[-1] - inventory_values[0], 2),
            'receivable_trend': round(receivable_values[-1] - receivable_values[0], 2),
            'payable_trend': round(payable_values[-1] - payable_values[0], 2),
        }
    
    @staticmethod
    def project_ccc_improvement(
        current_ccc: Dict[str, float],
        target_improvements: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Project improved CCC based on proposed improvements
        target_improvements: e.g., {'inventory_days': -10, 'receivable_days': -5}
        """
        improved = current_ccc.copy()
        
        for component, improvement in target_improvements.items():
            if component in improved:
                improved[component] = max(0, improved[component] + improvement)
        
        improved['ccc'] = improved['inventory_days'] + improved['receivable_days'] - improved['payable_days']
        
        return {
            'current': current_ccc,
            'projected': improved,
            'improvement': {
                'inventory_days': round(improved['inventory_days'] - current_ccc['inventory_days'], 2),
                'receivable_days': round(improved['receivable_days'] - current_ccc['receivable_days'], 2),
                'payable_days': round(improved['payable_days'] - current_ccc['payable_days'], 2),
                'ccc_improvement': round(improved['ccc'] - current_ccc['ccc'], 2),
            }
        }

    @staticmethod
    def compare_insights(
        company1_name: str,
        company2_name: str,
        ccc1: Dict[str, float],
        ccc2: Dict[str, float]
    ) -> List[str]:
        """Explain the operational meaning of differences between two CCC profiles."""
        insights = []
        differences = {
            'inventory': ccc1['inventory_days'] - ccc2['inventory_days'],
            'receivables': ccc1['receivable_days'] - ccc2['receivable_days'],
            'payables': ccc1['payable_days'] - ccc2['payable_days'],
            'ccc': ccc1['ccc'] - ccc2['ccc'],
        }

        faster = company1_name if differences['ccc'] < 0 else company2_name
        slower = company2_name if differences['ccc'] < 0 else company1_name
        gap = abs(differences['ccc'])
        if gap == 0:
            insights.append(f"Both companies have the same cash conversion cycle at {ccc1['ccc']:.1f} days.")
        else:
            insights.append(
                f"{faster} converts operating activity into cash faster: its CCC is {gap:.1f} days shorter than {slower}."
            )

        if abs(differences['receivables']) >= 5:
            higher = company1_name if differences['receivables'] > 0 else company2_name
            lower = company2_name if differences['receivables'] > 0 else company1_name
            insights.append(
                f"Collection is the clearest difference: {higher} waits {abs(differences['receivables']):.1f} more days for customers to pay than {lower}. "
                f"That gap points to differences in credit terms, customer mix, or collection discipline."
            )

        if abs(differences['inventory']) >= 5:
            higher = company1_name if differences['inventory'] > 0 else company2_name
            lower = company2_name if differences['inventory'] > 0 else company1_name
            insights.append(
                f"{higher} holds inventory for {abs(differences['inventory']):.1f} more days than {lower}, which may indicate slower stock movement or a deliberate availability buffer."
            )

        if abs(differences['payables']) >= 5:
            higher = company1_name if differences['payables'] > 0 else company2_name
            lower = company2_name if differences['payables'] > 0 else company1_name
            insights.append(
                f"{higher} takes {abs(differences['payables']):.1f} more days to pay suppliers than {lower}. This supports liquidity, provided supplier relationships and discounts are not being damaged."
            )

        for name, ccc in ((company1_name, ccc1['ccc']), (company2_name, ccc2['ccc'])):
            if ccc < 0:
                insights.append(
                    f"{name} has a negative CCC of {ccc:.1f} days: it receives cash from customers before paying for the related operating cycle, a strong working-capital advantage."
                )
            elif ccc > 90:
                insights.append(
                    f"{name} has a long CCC of {ccc:.1f} days, so more cash remains tied up between paying operating costs and collecting customer cash."
                )

        if not insights:
            insights.append("The component profiles are broadly similar; monitor the trend over multiple reporting periods before drawing a strong conclusion.")
        insights.append(
            "Read the comparison directionally: a lower CCC is generally better, but unusually low values should be checked for aggressive supplier terms or one-off period effects."
        )
        return insights

    @staticmethod
    def company_insights(historical: List[Dict[str, Any]], current: Dict[str, float]) -> List[str]:
        """Derive investor-oriented observations from CCC and statement trends."""
        insights = []
        if len(historical) < 2:
            return insights

        oldest, latest = historical[0], historical[-1]
        if oldest.get('revenue') and latest.get('revenue'):
            revenue_change = (latest['revenue'] - oldest['revenue']) / abs(oldest['revenue']) * 100
            insights.append(f"Revenue changed {revenue_change:+.1f}% across the available periods.")

        if oldest.get('revenue') and latest.get('inventory'):
            inventory_change = (latest['inventory'] - oldest['inventory']) / abs(oldest['inventory']) * 100 if oldest.get('inventory') else None
            if inventory_change is not None and inventory_change > 10:
                insights.append(f"Inventory grew {inventory_change:.1f}% over the period. Check whether stock growth is keeping pace with sales and whether slow-moving items are building up.")

        if oldest.get('revenue') and latest.get('receivables'):
            receivables_change = (latest['receivables'] - oldest['receivables']) / abs(oldest['receivables']) * 100 if oldest.get('receivables') else None
            if receivables_change is not None and receivables_change > 10:
                insights.append(f"Receivables grew {receivables_change:.1f}% over the period. Compare this with revenue growth because faster receivables growth can consume cash despite reported sales growth.")

        profits = [item.get('net_profit') for item in historical if item.get('net_profit') is not None]
        operating_cash = [item.get('operating_cash_flow') for item in historical if item.get('operating_cash_flow') is not None]
        if len(profits) >= 2 and len(operating_cash) >= 2:
            if profits[-1] > profits[0] and operating_cash[-1] < operating_cash[0]:
                insights.append("Net profit increased while operating cash flow declined across the available periods. Working capital movements may be absorbing cash, so profitability should not be viewed without cash-flow support.")
            cash_conversion = operating_cash[-1] / profits[-1] if profits[-1] else None
            if cash_conversion is not None:
                insights.append(f"Latest operating cash flow is {cash_conversion:.2f} times latest net profit. Values materially below 1.0 deserve review of receivables, inventory, payables, and non-cash accounting items.")

        if current['ccc'] < 0:
            insights.append(f"The current CCC is negative at {current['ccc']:.1f} days, meaning customer cash arrives before the operating cycle is fully funded. Check whether this reflects durable business economics or unusually extended supplier terms.")
        elif len(historical) >= 3:
            first_ccc = historical[0]['ccc']
            last_ccc = historical[-1]['ccc']
            if last_ccc > first_ccc:
                insights.append(f"CCC increased from {first_ccc:.1f} to {last_ccc:.1f} days. Growth may be requiring more cash to support the operating cycle, even if revenue and profit are rising.")

        return insights
