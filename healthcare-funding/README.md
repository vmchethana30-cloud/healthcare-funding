# 🏥 Healthcare Funding Analytics
## Activity Based Funding · Own Source Revenue · National Funding Arrangements

**Author:** Chethana Manjunath  
**Tools:** Python · Pandas · Matplotlib · Seaborn · Jupyter  
**Dataset:** Simulated Queensland public hospital funding data (14 HHS · 2019–2024)

---

## Project Overview

A comprehensive end-to-end analysis of Queensland public hospital funding across three streams:

- **Activity Based Funding (ABF)** — NWA volumes, prices, funded amounts and cost variances by HHS and care type
- **Own Source Revenue (OSR)** — Revenue trends, COVID-19 impact, category performance and budget variance
- **National Funding Arrangements (NFA)** — Commonwealth vs State split, stream utilisation and allocation trends

---

## Project Structure

```
healthcare-funding/
├── data/
│   ├── abf_data.csv              # 2,016 rows — ABF by HHS, year, quarter, care type
│   ├── osr_data.csv              # 3,024 rows — OSR by HHS, year, quarter, category
│   ├── nfa_data.csv              # 588 rows  — NFA by HHS, year, funding stream
│   └── funding_summary.csv       # 84 rows   — Consolidated summary by HHS and year
│
├── notebooks/
│   └── Healthcare_Funding_Analysis.ipynb   ← Main analysis notebook
│
├── src/
│   └── generate_data.py          # Generates all datasets
│
└── outputs/
    ├── chart_abf_by_hhs.png
    ├── chart_abf_trend.png
    ├── chart_abf_variance.png
    ├── chart_osr_trend.png
    ├── chart_osr_variance.png
    ├── chart_nfa_split.png
    ├── chart_nfa_utilisation.png
    ├── chart_indigenous_funding.png
    ├── chart_consolidated_dashboard.png
---
---

## Analysis Sections

| Section | Content |
|---------|---------|
| 1 | Setup, data loading, quality check |
| 2 | ABF — funding by HHS, trend, NWA price growth, cost variance |
| 3 | OSR — COVID impact, category breakdown, budget variance by HHS |
| 4 | NFA — Commonwealth/State split, stream utilisation, Indigenous health |
| 5 | Consolidated dashboard — all streams combined |
| 6 | Key findings summary |

---

## Key Findings

| Stream | Finding |
|--------|---------|
| **ABF** | NWA price grew 13.3% (2019–2024). ED and Mental Health show consistent cost overruns. COVID caused ~12% activity dip in 2020. |
| **OSR** | COVID reduced OSR by ~25% in 2020. Private Patient Fees (35%) dominate. Full recovery by 2023. |
| **NFA** | Commonwealth share growing from 50% → 52.5%. Capital Funding and Preventive Health below 95% utilisation target. |
| **Consolidated** | ABF = ~68% of total funding. NQ holds stable 14–15% share of QLD ABF. |

---

