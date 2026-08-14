import asyncio
import sys
from typing import Dict, Any

import pandas as pd
import streamlit as st

sys.path.insert(0, "backend")
from app.services.screener import screener_service
from app.services.ccc_analysis import CCCAnalysisService


st.set_page_config(
    page_title="BADYAL | CCC Analyzer",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
:root { color-scheme: dark; }
[data-testid="stAppViewContainer"] { background: #101827; }
[data-testid="stHeader"] { background: rgba(16, 24, 39, 0.92); }
.block-container { max-width: 1180px; padding-top: 2rem; }
.hero { padding: 2rem 0 1rem; }
.eyebrow { color: #7dd3fc; text-transform: uppercase; letter-spacing: .16em; font-size: .78rem; font-weight: 700; }
.hero h1 { font-size: clamp(2.4rem, 6vw, 4.8rem); line-height: 1; margin: .4rem 0 1rem; color: #f8fafc; }
.hero p { color: #cbd5e1; font-size: 1.1rem; max-width: 720px; }
.card { background: #172235; border: 1px solid #2a3a52; border-radius: 14px; padding: 1.2rem; margin: .7rem 0; }
.metric { background: #172235; border: 1px solid #2a3a52; border-radius: 14px; padding: 1rem; min-height: 120px; }
.metric-label { color: #94a3b8; font-size: .82rem; text-transform: uppercase; letter-spacing: .08em; }
.metric-value { color: #f8fafc; font-size: 2rem; font-weight: 800; margin-top: .45rem; }
.metric-unit { color: #7dd3fc; font-size: .86rem; }
.insight { border-left: 3px solid #38bdf8; padding: .75rem 1rem; margin: .6rem 0; background: #172235; color: #dbeafe; }
.warning { border-left-color: #fbbf24; }
.disclaimer { color: #94a3b8; font-size: .82rem; border-top: 1px solid #2a3a52; margin-top: 3rem; padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)


def run(coro):
    return asyncio.run(coro)


def company_identifier(company: Dict[str, Any]) -> str:
    url = company.get("url", "")
    if "/company/" in url:
        return url.split("/company/", 1)[1].split("/", 1)[0]
    return str(company.get("bse_code") or company.get("code") or company.get("id"))


def load_analysis(identifier: str):
    data = run(screener_service.get_company_data(identifier))
    if not data:
        raise ValueError("No financial data was returned for this company.")
    current = data.get("ccc_components") or CCCAnalysisService.calculate_ccc_components(data)
    benchmark = CCCAnalysisService.benchmark_for_industry(data.get("industry", ""))
    problems, assessment = CCCAnalysisService.identify_problems(
        current,
        benchmark_override=benchmark,
        available_components=data.get("data_quality", {}).get("available_components"),
    )
    historical = []
    for period in data.get("historical", []):
        if "ccc" in period:
            historical.append({
                "Period": period["period"],
                "CCC": period["ccc"],
                "Receivable Days": period["receivable_days"],
                "Inventory Days": period["inventory_days"],
                "Payable Days": period["payable_days"],
            })
    investor_insights = []
    if len(historical) >= 2:
        first, latest = historical[0], historical[-1]
        if latest["CCC"] > first["CCC"]:
            investor_insights.append(f"CCC increased from {first['CCC']:.1f} to {latest['CCC']:.1f} days, suggesting that growth may be consuming more working capital.")
        else:
            investor_insights.append(f"CCC moved from {first['CCC']:.1f} to {latest['CCC']:.1f} days, indicating improving cash conversion over the available periods.")
    return data, current, benchmark, problems, assessment, historical, investor_insights


st.markdown('<div class="hero"><div class="eyebrow">BADYAL / Academic Financial Screening</div><h1>Cash Conversion Cycle Analyzer</h1><p>Move from reported financial numbers to a structured, explainable first-level working-capital assessment.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("BADYAL")
    st.caption("Working-capital intelligence")
    st.markdown("Search a Screener-listed company, then review its CCC, industry reference, trends, and investor-oriented observations.")
    st.divider()
    st.caption("Source: Screener.in")

query = st.text_input("Company search", placeholder="Type a company name or Screener symbol", key="company_query")
selected = None
if len(query.strip()) >= 2:
    try:
        results = run(screener_service.search_company(query.strip()))[:8]
        if results:
            labels = [f"{item.get('name', 'Unknown')} · {company_identifier(item)}" for item in results]
            choice = st.selectbox("Choose a company", labels)
            selected = results[labels.index(choice)]
        else:
            st.info("No companies found.")
    except Exception as error:
        st.error(f"Company search failed: {error}")

if st.button("Analyze company", type="primary", disabled=selected is None):
    st.session_state["selected_identifier"] = company_identifier(selected)

identifier = st.session_state.get("selected_identifier")
if identifier:
    try:
        data, current, benchmark, problems, assessment, historical, investor_insights = load_analysis(identifier)
        st.markdown(f"## {data.get('company_name', identifier)}")
        st.caption(f"Screener identifier: {identifier} · Industry: {data.get('industry') or 'Not classified'}")

        columns = st.columns(4)
        metrics = [
            ("Inventory Days", current["inventory_days"]),
            ("Receivable Days", current["receivable_days"]),
            ("Payable Days", current["payable_days"]),
            ("Cash Conversion Cycle", current["ccc"]),
        ]
        for column, (label, value) in zip(columns, metrics):
            column.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value:.1f}</div><div class="metric-unit">days</div></div>', unsafe_allow_html=True)

        st.subheader("Working-capital assessment")
        st.markdown(f'<div class="card">{assessment}</div>', unsafe_allow_html=True)
        st.info(f"Industry reference: CCC {benchmark['ccc']} days; inventory {benchmark['inventory_days']} days; receivables {benchmark['receivable_days']} days; payables {benchmark['payable_days']} days. {benchmark['source']}.")

        if problems:
            st.subheader("Identified problems")
            for problem in problems:
                st.markdown(f'<div class="insight warning"><strong>{problem.problem_type.replace("_", " ").title()}</strong><br>{problem.description}<br><small>{problem.impact}</small></div>', unsafe_allow_html=True)
        else:
            st.success("No material working-capital problem was identified against the selected industry reference.")

        if historical:
            st.subheader("CCC trend")
            frame = pd.DataFrame(historical).set_index("Period")
            st.line_chart(frame[["CCC", "Receivable Days", "Inventory Days", "Payable Days"]])
            with st.expander("View annual data"):
                st.dataframe(frame, use_container_width=True)

        if investor_insights:
            st.subheader("Investor perspective")
            for insight in investor_insights:
                st.markdown(f'<div class="insight">{insight}</div>', unsafe_allow_html=True)

        st.caption(f"Data used: {data.get('data_quality', {}).get('source', 'Screener.in')}. Periods: {', '.join(data.get('data_quality', {}).get('periods_used', []))}.")
    except Exception as error:
        st.error(f"Analysis failed: {error}")
else:
    st.markdown('<div class="card">Search for a listed company above to begin the BADYAL analysis.</div>', unsafe_allow_html=True)

st.markdown('<div class="disclaimer"><strong>Academic disclaimer:</strong> BADYAL is an academic project for educational analysis only. It should not be used to make investment decisions. Always verify financial information against company filings and consult a qualified professional.</div>', unsafe_allow_html=True)
