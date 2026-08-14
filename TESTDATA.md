# Sample Test Data for Development

This file contains sample financial data for testing without live Screener.in integration.

## Sample Company 1: ABC Manufacturing

```json
{
  "company_name": "ABC Manufacturing Ltd",
  "bse_code": "500001",
  "sector": "manufacturing",
  "financial_metrics": {
    "average_inventory": 5000000,
    "cost_of_goods_sold": 40000000,
    "average_receivables": 3000000,
    "revenue": 35000000,
    "average_payables": 4000000
  },
  "profitability_data": {
    "net_profit_margin": 15.5,
    "return_on_equity": 22.3,
    "return_on_assets": 10.2
  }
}
```

**Expected CCC Calculation:**
- Inventory Days = (5000000 / 40000000) * 365 = 45.6 days
- Receivable Days = (3000000 / 35000000) * 365 = 31.3 days
- Payable Days = (4000000 / 40000000) * 365 = 36.5 days
- CCC = 45.6 + 31.3 - 36.5 = 40.4 days

## Sample Company 2: XYZ Retail

```json
{
  "company_name": "XYZ Retail Corp",
  "bse_code": "500002",
  "sector": "retail",
  "financial_metrics": {
    "average_inventory": 2000000,
    "cost_of_goods_sold": 25000000,
    "average_receivables": 1000000,
    "revenue": 30000000,
    "average_payables": 3500000
  },
  "profitability_data": {
    "net_profit_margin": 8.5,
    "return_on_equity": 18.5,
    "return_on_assets": 9.0
  }
}
```

**Expected CCC Calculation:**
- Inventory Days = (2000000 / 25000000) * 365 = 29.2 days
- Receivable Days = (1000000 / 30000000) * 365 = 12.2 days
- Payable Days = (3500000 / 25000000) * 365 = 51.1 days
- CCC = 29.2 + 12.2 - 51.1 = -9.7 days (Excellent efficiency!)

## Comparison Insights

When comparing ABC Manufacturing vs XYZ Retail:
- ABC has 50.1 days higher CCC → Less efficient
- ABC takes longer to sell inventory (45.6 vs 29.2 days)
- XYZ has better customer collections (12.2 vs 31.3 days)
- XYZ negotiates better supplier terms (51.1 vs 36.5 days)

## Historical Data Example (5 years)

For testing trend analysis:

```json
[
  {"period": "2019", "inventory_days": 60.0, "receivable_days": 35.0, "payable_days": 30.0, "ccc": 65.0},
  {"period": "2020", "inventory_days": 55.0, "receivable_days": 33.0, "payable_days": 32.0, "ccc": 56.0},
  {"period": "2021", "inventory_days": 50.0, "receivable_days": 31.0, "payable_days": 35.0, "ccc": 46.0},
  {"period": "2022", "inventory_days": 48.0, "receivable_days": 30.0, "payable_days": 36.0, "ccc": 42.0},
  {"period": "2023", "inventory_days": 45.6, "receivable_days": 31.3, "payable_days": 36.5, "ccc": 40.4}
]
```

**Trend Analysis Result:**
- CCC Trend: Improving ✅
- Total Change: -24.6 days (excellent improvement!)
- Average Change: -6.15 days per year

## How to Use This Data

### For Manual Testing:

1. Create a file: `backend/test_data.json`
2. Modify `ScreenerService` to return this data when in test mode
3. Use for frontend testing without API dependencies

### Modify the Screener Service:

```python
# In app/services/screener.py

async def get_company_data(self, bse_code: str):
    # Development mode: return sample data
    if os.getenv("ENVIRONMENT") == "development":
        return self._get_sample_data(bse_code)
    
    # Production: call real API
    return await self._fetch_from_screener(bse_code)

def _get_sample_data(self, bse_code: str):
    samples = {
        "500001": self.ABC_MANUFACTURING,
        "500002": self.XYZ_RETAIL
    }
    return samples.get(bse_code, {})
```

## Using Test Data for Development

To enable test data mode:

1. Set environment variable:
```bash
export ENVIRONMENT=development
python main.py
```

2. Or add to `.env`:
```
ENVIRONMENT=development
```

3. Frontend will still work normally
4. Backend returns sample data instead of calling Screener.in

This allows full development and testing without API dependencies!
