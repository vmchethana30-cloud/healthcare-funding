"""
generate_data.py
Generates realistic simulated healthcare funding datasets covering:
  1. Activity Based Funding (ABF)
  2. Own Source Revenue (OSR)
  3. National Funding Arrangements (NFA)

All data is modelled on Queensland public hospital funding structures.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ── Constants ──────────────────────────────────────────────────
HHS_LIST = [
    'Cairns and Hinterland', 'Townsville', 'Mackay',
    'North West', 'Torres and Cape', 'Metro North',
    'Metro South', 'Gold Coast', 'Sunshine Coast',
    'West Moreton', 'Darling Downs', 'Central Queensland',
    'Wide Bay', 'South West'
]

YEARS     = [2019, 2020, 2021, 2022, 2023, 2024]
QUARTERS  = ['Q1', 'Q2', 'Q3', 'Q4']

CARE_TYPES = ['Admitted Acute', 'Admitted Subacute', 'Emergency Department',
              'Outpatient', 'Mental Health', 'Maternity']

ACTIVITY_TYPES = ['Inpatient', 'Same Day', 'Emergency', 'Outpatient', 'Subacute']

OSR_CATEGORIES = ['Car Parking', 'Cafeteria & Food Services', 'Private Patient Fees',
                  'Pharmacy Retail', 'Medical Imaging (Private)', 'Accommodation Fees',
                  'Equipment Hire', 'Research Grants', 'Other Commercial']

NFA_STREAMS = ['National Health Reform Agreement', 'Mental Health', 'Preventive Health',
               'Indigenous Health', 'Public Health', 'Capital Funding', 'Teaching & Research']

# Base NWA (National Weighted Activity) by HHS — larger HHS get more
BASE_NWA = {
    'Metro North': 420000, 'Metro South': 390000, 'Gold Coast': 280000,
    'Sunshine Coast': 210000, 'West Moreton': 140000, 'Cairns and Hinterland': 130000,
    'Townsville': 145000, 'Darling Downs': 120000, 'Central Queensland': 110000,
    'Wide Bay': 95000, 'Mackay': 80000, 'North West': 25000,
    'Torres and Cape': 18000, 'South West': 15000
}

# NWA price per unit ($)
NWA_PRICE = {2019: 5012, 2020: 5127, 2021: 5234, 2022: 5389, 2023: 5512, 2024: 5678}

# ── 1. ABF Dataset ─────────────────────────────────────────────
print("Generating ABF dataset...")
abf_rows = []
for hhs in HHS_LIST:
    base = BASE_NWA[hhs]
    for year in YEARS:
        for qtr in QUARTERS:
            for care in CARE_TYPES:
                # Care type weight
                weight = {'Admitted Acute': 0.40, 'Emergency Department': 0.22,
                          'Outpatient': 0.18, 'Admitted Subacute': 0.09,
                          'Mental Health': 0.07, 'Maternity': 0.04}[care]
                # Growth trend + COVID dip in 2020
                growth = 1.0 + (year - 2019) * 0.025
                if year == 2020: growth *= 0.88
                if year == 2021: growth *= 0.94

                nwa = base * weight * growth / 4 * np.random.uniform(0.92, 1.08)
                price = NWA_PRICE[year]
                funded = nwa * price
                actual_cost = funded * np.random.uniform(0.95, 1.12)
                variance = funded - actual_cost

                abf_rows.append({
                    'HHS': hhs, 'Year': year, 'Quarter': qtr,
                    'Care_Type': care,
                    'NWA_Units': round(nwa, 1),
                    'NWA_Price': price,
                    'ABF_Funded_Amt': round(funded, 0),
                    'Actual_Cost': round(actual_cost, 0),
                    'Variance': round(variance, 0),
                    'Variance_Pct': round(variance / funded * 100, 2),
                    'FY': f"FY{year}/{str(year+1)[-2:]}",
                })

abf = pd.DataFrame(abf_rows)
abf.to_csv('../data/abf_data.csv', index=False)
print(f"  abf_data.csv — {len(abf):,} rows")

# ── 2. Own Source Revenue Dataset ──────────────────────────────
print("Generating OSR dataset...")
osr_rows = []
# OSR base scales roughly with HHS size
OSR_BASE = {h: BASE_NWA[h] * 0.008 for h in HHS_LIST}

for hhs in HHS_LIST:
    base = OSR_BASE[hhs]
    for year in YEARS:
        for qtr in QUARTERS:
            for cat in OSR_CATEGORIES:
                cat_weight = {
                    'Private Patient Fees': 0.35, 'Car Parking': 0.18,
                    'Pharmacy Retail': 0.12, 'Cafeteria & Food Services': 0.10,
                    'Medical Imaging (Private)': 0.09, 'Research Grants': 0.07,
                    'Accommodation Fees': 0.04, 'Equipment Hire': 0.03,
                    'Other Commercial': 0.02
                }[cat]
                growth = 1.0 + (year - 2019) * 0.03
                if year == 2020: growth *= 0.75  # COVID hit OSR hard
                if year == 2021: growth *= 0.88

                revenue = base * cat_weight * growth * np.random.uniform(0.88, 1.12) * 1000
                budget  = revenue * np.random.uniform(0.90, 1.10)
                variance = revenue - budget

                osr_rows.append({
                    'HHS': hhs, 'Year': year, 'Quarter': qtr,
                    'Category': cat,
                    'Actual_Revenue': round(revenue, 0),
                    'Budgeted_Revenue': round(budget, 0),
                    'Variance': round(variance, 0),
                    'Variance_Pct': round(variance / budget * 100, 2) if budget else 0,
                    'FY': f"FY{year}/{str(year+1)[-2:]}",
                })

osr = pd.DataFrame(osr_rows)
osr.to_csv('../data/osr_data.csv', index=False)
print(f"  osr_data.csv — {len(osr):,} rows")

# ── 3. National Funding Arrangements Dataset ───────────────────
print("Generating NFA dataset...")
nfa_rows = []

# Commonwealth / State split — 50/50 base shifting to 45/55 by 2024
COMMONWEALTH_SHARE = {2019: 0.500, 2020: 0.505, 2021: 0.510,
                      2022: 0.515, 2023: 0.520, 2024: 0.525}

NFA_BASE = {h: BASE_NWA[h] * NWA_PRICE[2019] * 0.85 for h in HHS_LIST}

for hhs in HHS_LIST:
    base = NFA_BASE[hhs]
    for year in YEARS:
        for stream in NFA_STREAMS:
            stream_weight = {
                'National Health Reform Agreement': 0.55,
                'Mental Health': 0.12, 'Indigenous Health': 0.08,
                'Teaching & Research': 0.07, 'Public Health': 0.07,
                'Capital Funding': 0.06, 'Preventive Health': 0.05
            }[stream]

            # Indigenous streams higher for NQ
            if stream == 'Indigenous Health' and hhs in ['Torres and Cape', 'North West', 'Cairns and Hinterland']:
                stream_weight *= 2.5

            growth = 1.0 + (year - 2019) * 0.032
            total  = base * stream_weight * growth * np.random.uniform(0.96, 1.04)
            cwth   = total * COMMONWEALTH_SHARE[year]
            state  = total - cwth
            drawn  = total * np.random.uniform(0.93, 1.00)
            undrawn = total - drawn

            nfa_rows.append({
                'HHS': hhs, 'Year': year,
                'Funding_Stream': stream,
                'Total_Allocation': round(total, 0),
                'Commonwealth_Share': round(cwth, 0),
                'State_Share': round(state, 0),
                'Commonwealth_Pct': round(COMMONWEALTH_SHARE[year] * 100, 1),
                'Amount_Drawn': round(drawn, 0),
                'Amount_Undrawn': round(undrawn, 0),
                'Utilisation_Pct': round(drawn / total * 100, 2),
                'FY': f"FY{year}/{str(year+1)[-2:]}",
            })

nfa = pd.DataFrame(nfa_rows)
nfa.to_csv('../data/nfa_data.csv', index=False)
print(f"  nfa_data.csv — {len(nfa):,} rows")

# ── 4. Consolidated Funding Summary ───────────────────────────
print("Generating consolidated summary...")
abf_sum = abf.groupby(['HHS','Year'])['ABF_Funded_Amt'].sum().reset_index().rename(columns={'ABF_Funded_Amt':'ABF_Total'})
osr_sum = osr.groupby(['HHS','Year'])['Actual_Revenue'].sum().reset_index().rename(columns={'Actual_Revenue':'OSR_Total'})
nfa_sum = nfa.groupby(['HHS','Year'])['Total_Allocation'].sum().reset_index().rename(columns={'Total_Allocation':'NFA_Total'})

summary = abf_sum.merge(osr_sum, on=['HHS','Year']).merge(nfa_sum, on=['HHS','Year'])
summary['Total_Funding'] = summary['ABF_Total'] + summary['OSR_Total'] + summary['NFA_Total']
summary['ABF_Pct'] = (summary['ABF_Total'] / summary['Total_Funding'] * 100).round(1)
summary['OSR_Pct'] = (summary['OSR_Total'] / summary['Total_Funding'] * 100).round(1)
summary['NFA_Pct'] = (summary['NFA_Total'] / summary['Total_Funding'] * 100).round(1)
summary.to_csv('../data/funding_summary.csv', index=False)
print(f"  funding_summary.csv — {len(summary):,} rows")

print("\nAll datasets generated successfully.")
print(f"  ABF rows:     {len(abf):,}")
print(f"  OSR rows:     {len(osr):,}")
print(f"  NFA rows:     {len(nfa):,}")
print(f"  Summary rows: {len(summary):,}")
