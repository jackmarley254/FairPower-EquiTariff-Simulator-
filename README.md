
# EquiTariff Simulator – Data Validation

## Overview
This repository contains datasets and validation work for Team FairPower’s EquiTariff Simulator. The focus is on preparing clean, reproducible data for clustering and affordability analysis.

## Contents
- **county_subcounty_validation.ipynb** → Notebook with validation tests and Markdown notes.
- **Households, 2019.csv** → Household counts dataset.
- **Chapter 9-Energy Tables.csv** → Energy reference data.
- **Average Electricity Yield.csv** → Yield dataset.
- **API_EG.ELC.ACCS.ZS_DS2_en_csv_v2_158.csv** → Electricity access dataset.
- **subcounty_to_county_mapping.json / .pkl** → Clean dictionary mapping subcounties to counties.

## Key Decisions
- County rows are unreliable → excluded from workflow.
- Subcounty aggregation adopted → county totals rebuilt from subcounty sums.
- Dictionary validated → 47 counties, 333 subcounties, no missing entries.

## Next Steps for Joel
- Use the validated subcounty dataset in `feature/data-prep`.
- Merge synthetic households (10,000+) with clean dataset.
- Run clustering models in `feature/clustering-engine`.
- Produce segment labels, profiles, and affordability metrics.


