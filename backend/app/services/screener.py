import re
import time
import requests
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup

class ScreenerService:
    """Service to interact with Screener.in for financial data"""
    
    BASE_URL = "https://www.screener.in/api"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
    
    async def search_company(self, query: str) -> List[Dict[str, Any]]:
        """Search for companies by name or BSE code"""
        try:
            # Using screener.in search endpoint
            url = f"{self.BASE_URL}/company/search/?q={query}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error searching company: {e}")
            return []
    
    # Screener renders consolidated figures by default and only falls back to
    # standalone when a company publishes no consolidated statements.
    STATEMENT_VARIANTS = (('consolidated/', 'consolidated'), ('', 'standalone'))
    MAX_ATTEMPTS = 4

    def _get_with_retry(self, url: str):
        """GET a Screener URL, retrying transient throttling/server errors."""
        last_error = None
        for attempt in range(self.MAX_ATTEMPTS):
            try:
                response = self.session.get(url, timeout=15)
            except requests.RequestException as exc:
                last_error = exc
            else:
                if response.status_code == 404:
                    return None
                if response.status_code < 400:
                    return response
                last_error = f'HTTP {response.status_code}'
                if response.status_code not in (429, 500, 502, 503, 504):
                    break
            if attempt < self.MAX_ATTEMPTS - 1:
                time.sleep(1.5 * (2 ** attempt))
        raise ValueError(f'Screener request failed for {url}: {last_error}')

    def _fetch_company_page(self, bse_code: str):
        """Return (soup, variant, url) for the statement Screener shows by default.

        Standalone is used only when Screener has no consolidated page at all. A
        throttled or malformed consolidated response raises instead of silently
        falling back, since that would report a different set of figures.
        """
        for path, variant in self.STATEMENT_VARIANTS:
            url = f"https://www.screener.in/company/{bse_code}/{path}"
            response = self._get_with_retry(url)
            if response is None:
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.select_one('section#ratios') or variant == 'standalone':
                return soup, variant, url
            raise ValueError(f'Screener returned no ratios section for {url}')
        raise ValueError(f'Screener page unavailable for {bse_code}')

    async def get_company_data(self, bse_code: str) -> Dict[str, Any]:
        """Fetch financial data for a company from Screener.in"""
        try:
            soup, variant, url = self._fetch_company_page(bse_code)
            return await self._parse_company_page(soup, bse_code, variant, url)
        except Exception as e:
            print(f"Error fetching company data for {bse_code}: {e}")
            return {}
    
    async def _parse_company_page(self, soup: BeautifulSoup, bse_code: str,
                                  statement_type: str = 'consolidated',
                                  source_url: str = '') -> Dict[str, Any]:
        """Parse annual operating and balance-sheet data from a Screener page."""

        profit_loss = self._read_table(soup, 'profit-loss')
        balance_sheet = self._read_table(soup, 'balance-sheet')
        periods = self._table_periods(soup, 'profit-loss') or self._table_periods(soup, 'balance-sheet')
        cash_flow = self._read_table(soup, 'cash-flow')
        cash_flow_periods = self._table_periods(soup, 'cash-flow')
        ratio_rows, ratio_periods = self._read_operating_ratios(soup)
        industry = self._industry(soup)

        debtor_days = self._find_row(ratio_rows, 'debtor days', 'debtors days', 'receivable days')
        ratio_inventory_days = self._find_row(ratio_rows, 'inventory days', 'stock days', 'inventory')
        ratio_payable_days = self._find_row(ratio_rows, 'days payable', 'payable days', 'days payables outstanding')
        ratio_ccc = self._find_row(ratio_rows, 'cash conversion cycle', 'ccc')
        if debtor_days and ratio_ccc:
            periods = ratio_periods or periods
            historical = []
            for index, ccc in enumerate(ratio_ccc):
                if ccc is None or index >= len(debtor_days) or debtor_days[index] is None:
                    continue
                inventory_days = ratio_inventory_days[index] if index < len(ratio_inventory_days) else 0
                payable_days = ratio_payable_days[index] if index < len(ratio_payable_days) else 0

                historical.append({
                    'period': periods[index] if index < len(periods) else f'Period {index + 1}',
                    'inventory_days': inventory_days or 0,
                    'receivable_days': debtor_days[index],
                    'payable_days': payable_days or 0,
                    'ccc': ccc,
                })
            if historical:
                sales = self._find_row(profit_loss, 'sales', 'revenue')
                net_profit = self._find_row(profit_loss, 'net profit')
                operating_cash = self._find_row(cash_flow, 'cash from operating activity')
                profit_periods = self._table_periods(soup, 'profit-loss')
                profit_by_period = self._period_values(profit_periods, sales, net_profit)
                cash_by_period = self._period_values(cash_flow_periods, operating_cash)
                for item in historical:
                    item.update(profit_by_period.get(item['period'], {}))
                    item.update(cash_by_period.get(item['period'], {}))
                latest = historical[-1]
                inventory_available = ratio_inventory_days and ratio_inventory_days[-1] is not None
                payable_available = ratio_payable_days and ratio_payable_days[-1] is not None
                return {
                    'bse_code': bse_code,
                    'company_name': self._text(soup.select_one('h1')) or bse_code,
                    'sector': '',
                    'industry': industry,
                    'ccc_components': {
                        'inventory_days': latest['inventory_days'],
                        'receivable_days': latest['receivable_days'],
                        'payable_days': latest['payable_days'],
                        'ccc': latest['ccc'],
                    },
                    'data_quality': {
                        'source': f'Screener.in {statement_type} ratios table',
                        'source_url': source_url,
                        'statement_type': statement_type,
                        'periods_used': [item['period'] for item in historical],
                        'cogs_note': 'CCC components are the ratios published by Screener. Blank component rows are excluded from problem flags and shown as zero only because Screener publishes CCC using the available components.',
                        'available_components': {
                            'inventory_days': bool(inventory_available),
                            'receivable_days': True,
                            'payable_days': bool(payable_available),
                        }
                    },
                    'historical': historical,
                }

        sales = self._find_row(profit_loss, 'sales', 'revenue', 'sales growth')
        expenses = self._find_row(profit_loss, 'expenses', 'cost of goods sold', 'cost of sales')
        inventories = self._find_row(balance_sheet, 'inventories', 'inventory')
        receivables = self._find_row(balance_sheet, 'trade receivables', 'receivables', 'accounts receivable')
        payables = self._find_row(balance_sheet, 'trade payables', 'payables', 'accounts payable')

        annual_count = min(len(sales), len(expenses), len(inventories), len(receivables), len(payables))
        historical = []
        for index in range(annual_count):
            if any(value is None for value in (
                sales[index], expenses[index], inventories[index], receivables[index], payables[index]
            )):
                continue
            historical.append({
                'period': periods[index] if index < len(periods) else f'Period {index + 1}',
                'revenue': sales[index],
                'cost_of_goods_sold': expenses[index],
                'inventory': inventories[index],
                'receivables': receivables[index],
                'payables': payables[index],
            })

        if not historical:
            raise ValueError('Screener page did not contain complete annual working-capital data')

        latest = historical[0]
        previous = historical[1] if len(historical) > 1 else latest
        company_name = self._text(soup.select_one('h1')) or bse_code

        return {
            'bse_code': bse_code,
            'company_name': company_name,
            'sector': '',
            'industry': industry,
            'revenue': latest['revenue'],
            'cost_of_goods_sold': latest['cost_of_goods_sold'],
            'average_inventory': (latest['inventory'] + previous['inventory']) / 2,
            'average_receivables': (latest['receivables'] + previous['receivables']) / 2,
            'average_payables': (latest['payables'] + previous['payables']) / 2,
            'data_quality': {
                'source': f'Screener.in {statement_type} profit-loss and balance-sheet tables',
                'source_url': source_url,
                'statement_type': statement_type,
                'periods_used': [item['period'] for item in historical],
                'cogs_note': 'Expenses are used as the closest available COGS proxy from Screener annual statements.'
            },
            'historical': historical,
        }

    @staticmethod
    def _text(element) -> str:
        return element.get_text(' ', strip=True) if element else ''

    def _industry(self, soup: BeautifulSoup) -> str:
        link = soup.select_one('a[title="Industry"]')
        return self._text(link)

    def _read_table(self, soup: BeautifulSoup, table_id: str) -> Dict[str, List[Optional[float]]]:
        table = soup.select_one(f'#{table_id}')
        if not table:
            return {}
        rows = {}
        for row in table.select('tbody tr'):
            cells = row.select('th, td')
            if len(cells) < 2:
                continue
            label = self._normalise_label(self._text(cells[0]))
            values = [self._parse_number(self._text(cell)) for cell in cells[1:]]
            rows[label] = values
        return rows

    def _table_periods(self, soup: BeautifulSoup, table_id: str) -> List[str]:
        table = soup.select_one(f'#{table_id}')
        if not table:
            return []
        header = table.select_one('thead tr')
        return [self._text(cell) for cell in header.select('th, td')[1:]] if header else []

    @staticmethod
    def _period_values(periods: List[str], *rows: List[Optional[float]]) -> Dict[str, Dict[str, Optional[float]]]:
        names = ('revenue', 'net_profit') if len(rows) == 2 else ('operating_cash_flow',)
        result = {}
        for index, period in enumerate(periods):
            values = {name: row[index] for name, row in zip(names, rows) if index < len(row)}
            if values:
                result[period] = values
        return result

    def _read_operating_ratios(self, soup: BeautifulSoup):
        """Read Screener's published 'Ratios' table verbatim."""
        table = None
        section = soup.select_one('section#ratios')
        if section:
            table = section.find('table')
        if table is None:
            for candidate in soup.find_all('table'):
                labels = [self._normalise_label(self._text(cell))
                          for cell in candidate.select('tbody tr th, tbody tr td.text')]
                if any('cash conversion' in label for label in labels):
                    table = candidate
                    break
        if table is None:
            return {}, []

        rows = {}
        for row in table.select('tbody tr'):
            cells = row.select('th, td')
            if len(cells) < 2:
                continue
            label = self._normalise_label(self._text(cells[0]))
            rows[label] = [self._parse_number(self._text(cell)) for cell in cells[1:]]
        header = table.select_one('thead tr')
        periods = [self._text(cell) for cell in header.select('th, td')[1:]] if header else []
        return rows, periods

    @staticmethod
    def _find_row(rows: Dict[str, List[Optional[float]]], *names: str) -> List[Optional[float]]:
        for name in names:
            normalised = ScreenerService._normalise_label(name)
            for label, values in rows.items():
                if label == normalised or label.startswith(normalised):
                    return values
        # If exact match not found, try partial matching for specific terms
        for name in names:
            for label, values in rows.items():
                label_lower = label.lower()
                if 'debtor' in name.lower() and ('debtor' in label_lower or 'receivable' in label_lower):
                    return values
                elif 'inventory' in name.lower() and 'inventory' in label_lower:
                    return values
                elif 'payable' in name.lower() and ('payable' in label_lower or 'payable outstanding' in label_lower):
                    return values
                elif 'cash conversion' in name.lower() and 'cash conversion' in label_lower:
                    return values
        return []

    @staticmethod
    def _normalise_label(value: str) -> str:
        # Remove special characters and convert to lowercase
        normalized = re.sub(r'[^a-z0-9 ]', '', value.lower()).strip()
        # Remove extra spaces
        normalized = ' '.join(normalized.split())
        return normalized

    @staticmethod
    def _parse_number(value: str) -> Optional[float]:
        cleaned = value.replace(',', '').replace('%', '').strip()
        if not cleaned or cleaned in {'-', '—', 'nan'}:
            return None
        multiplier = 1
        if cleaned.endswith('Cr'):
            cleaned = cleaned[:-2].strip()
        elif cleaned.endswith('Lakh'):
            cleaned = cleaned[:-4].strip()
            multiplier = 0.01
        try:
            return float(cleaned) * multiplier
        except ValueError:
            return None
    
    async def get_historical_financials(self, bse_code: str, years: int = 5) -> Dict[str, Any]:
        """Fetch historical financial data"""
        try:
            url = f"https://www.screener.in/api/company/{bse_code}/financials/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return {}

# Initialize service
screener_service = ScreenerService()
