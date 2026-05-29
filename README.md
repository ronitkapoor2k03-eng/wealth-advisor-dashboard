# Wealth Management Dashboard: Role of Financial Advisors in India (2010–2025)

## Overview
Interactive dashboard analysing 16 years of India's wealth management ecosystem using real data from AMFI, SEBI, World Bank, and CFA Institute.

## Key Features
- Growth trends for AUM, Folios, Literacy, Trust, and Advisor Count
- Correlation heatmap
- Advisor Paradox visualisation (AUM up, advisors down)
- **Elasticity Calculator** (using log-log regression: 2.82 elasticity)
- Regression summary tables
- Data quality tracker

## Data Sources
| Variable | Source |
|----------|--------|
| AUM & Folios | AMFI (amfiindia.com) |
| Registered Advisors | SEBI (sebi.gov.in) |
| Financial Literacy | World Bank Global Findex + SEBI 2025 |
| Trust in Advisors | CFA Institute 2025 |

## Running Locally
```bash
pip install -r requirements.txt
streamlit run app.py
