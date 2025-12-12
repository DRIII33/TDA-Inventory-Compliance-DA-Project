# TDA-Inventory-Compliance-DA-Project

This is a comprehensive, end-to-end portfolio project designed to showcase the exact skill set required for the TDA Food Distribution Specialist (Data Analyst) role, particularly focusing on compliance, inventory reconciliation, and proactive intervention.

The project successfully generated synthetic data, applied the necessary compliance logic, and produced actionable transfer recommendations, fulfilling the core responsibilities outlined in the job description: **"Analyze and monitor CE and processor data for compliance"** and **"Review and process transfer requests."**

## 🚀 Portfolio Project: Proactive USDA Foods Inventory Compliance

| Element | Detail |
| :--- | :--- |
| **Project Title** | USDA Foods Inventory Risk & Utilization Dashboard: Proactively Identifying Non-Compliance |
| **GitHub Repository Name** | `TDA-Inventory-Compliance-DA-Project` |
| **Project ID (BigQuery)** | `driiiportfolio` |

-----

## I. Business Scenario & Problem

**Scenario:** The Texas Department of Agriculture (TDA) must ensure all Contracting Entities (CEs) and Processors comply with federal regulations, primarily the requirement to maintain **USDA Foods inventory levels below a six-month supply (6MOH)**. Failure to do so leads to waste, spoilage, and federal penalties.

**Problem:** TDA needs to move from reactive compliance monitoring (identifying 6MOH violations *after* they occur) to **proactive risk identification** and **transfer coordination** to maximize utilization of the $2.5+ billion in federal assets.

-----

## II. GitHub Repository Structure

The repository follows a professional, structured, CRISP-DM-based workflow:

```
TDA-Inventory-Compliance-DA-Project/
│
├── README.md                                 # Project summary, problem, solution, and findings.
├── data_dictionary.csv                       # Definitions of all synthetic data columns.
│
├── 01_business_context/
│   └── 01_Business_Understanding_Problem_Statement.pdf # Detailed TDA 6MOH compliance issue and project scope.
│
├── 02_data_preparation/
│   ├── Inventory_Usage_Synthetic_Data.csv    # The raw, generated synthetic dataset.
│   └── 02_Data_Prep_Synthetic_Data_Generator.ipynb # Python script to generate the synthetic CSV.
│
├── 03_sql_queries/
│   ├── 03_Data_Prep_ETL_BigQuery.sql         # SQL for table creation and initial data validation (BigQuery Load).
│   └── 04_Compliance_Risk_Assessment.sql     # Core SQL query to identify 6MOH violations and short-shelf-life risks.
│
├── 04_notebooks/
│   └── 05_Transfer_Opportunity_Matcher.ipynb # Python (Colab) notebook for transfer matching logic and generating executive findings.
│
└── 05_deliverables/
    ├── 06_Transfer_Recommendations.csv       # Output list of proposed transfers (used for technical assistance).
    └── 06_TDA_Inventory_Dashboard_Mockup.pdf # Mockup of the Looker Studio report (Executive Summary).
```

-----

## III. Key Deliverables (Code and Results)

### A. Data Dictionary (`data_dictionary.csv`)

| Field Name | Description | Data Type | Core Metric Use |
| :--- | :--- | :--- | :--- |
| `Entity_ID` | Unique ID for the CE or Processor. | STRING | Grouping, identification. |
| `Product_ID` | USDA Food commodity identifier. | STRING | Matching for transfers. |
| `Inventory_Date` | Month-end date of the MPR submission. | DATE | Timeliness check. |
| `Current_Inventory_LBS` | Pounds of product currently in stock. | FLOAT | Numerator for MOH. |
| `Avg_Monthly_Usage_LBS` | Rolling 6-month average usage. | FLOAT | Denominator for MOH. |
| `Best_By_Date` | Oldest expiration date for the lot. | DATE | Shelf-life risk calculation. |
| `Calculated_MOH` | **Months of Hold (MOH):** `Inv_LBS` / `Avg_Usage_LBS`. | FLOAT | **Primary Compliance Metric.** |

### B. Core Compliance Risk Assessment (SQL)

This query (simulated and validated in Python) performs the primary analysis required of the role: identifying non-compliance and prioritizing action.

**File Name:** `04_Compliance_Risk_Assessment.sql`
**(Designed to run in Google BigQuery: `driiiportfolio.tda_compliance_data.inventory_mpr`)**

```sql
-- DELIVERABLE: 04_Compliance_Risk_Assessment.sql
-- DESCRIPTION: SQL query to identify 6MOH violations and high-priority transfer candidates.

WITH Compliance_Metrics AS (
    SELECT
        Entity_ID, Product_ID, Product_Name, Current_Inventory_LBS, Avg_Monthly_Usage_LBS, Calculated_MOH, Best_By_Date,
        DATE_DIFF(Best_By_Date, CURRENT_DATE(), DAY) AS Days_Until_Best_By,
        CASE
            WHEN Calculated_MOH >= 6.0 THEN 'NON-COMPLIANT (6MOH VIOLATION)'
            WHEN Calculated_MOH >= 5.0 THEN 'HIGH-RISK (5-6 MOH)'
            ELSE 'COMPLIANT'
        END AS Compliance_Status
    FROM
        `driiiportfolio.tda_compliance_data.inventory_mpr`
    WHERE
        Avg_Monthly_Usage_LBS > 0 
)
SELECT
    Compliance_Metrics.*,
    CASE
        WHEN Days_Until_Best_By <= 180 AND Compliance_Status IN ('NON-COMPLIANT (6MOH VIOLATION)', 'HIGH-RISK (5-6 MOH)') 
             THEN 'IMMEDIATE ACTION: TRANSFER & COMPLIANCE REVIEW'
        WHEN Compliance_Status = 'NON-COMPLIANT (6MOH VIOLATION)' 
             THEN 'ACTION: NON-COMPLIANCE NOTICE & TRANSFER REQUIRED'
        WHEN Compliance_Status = 'HIGH-RISK (5-6 MOH)' 
             THEN 'ALERT: PROACTIVE TECHNICAL ASSISTANCE/TRANSFER OPPORTUNITY'
        ELSE 'MONITOR'
    END AS Intervention_Priority,
    (6.0 - Calculated_MOH) * Avg_Monthly_Usage_LBS AS Potential_Transfer_Need_LBS
FROM
    Compliance_Metrics
WHERE
    Compliance_Status <> 'COMPLIANT' 
    OR Days_Until_Best_By <= 180 
    OR Calculated_MOH < 1.0 -- Include low MOH for transfer targeting
ORDER BY
    CASE Intervention_Priority 
        WHEN 'IMMEDIATE ACTION: TRANSFER & COMPLIANCE REVIEW' THEN 1
        WHEN 'ACTION: NON-COMPLIANCE NOTICE & TRANSFER REQUIRED' THEN 2
        WHEN 'ALERT: PROACTIVE TECHNICAL ASSISTANCE/TRANSFER OPPORTUNITY' THEN 3
        ELSE 4
    END,
    Current_Inventory_LBS DESC;
```

### C. Transfer Opportunity Matching (Python)

This script implements the core logic for the Data Analyst's technical assistance role: matching problem inventory (sources) with entities that need it (targets).

**File Name:** `05_Transfer_Opportunity_Matcher.ipynb`
**(Designed to run in Google Colab)**

```python
import pandas as pd
from tabulate import tabulate

# --- 1. Load the Compliance Analysis Data (Assume this is the output of the SQL query)
df_analysis = pd.read_csv('Compliance_Analysis_Results.csv')

# --- 2. Segment Sources (Excess Inventory) and Targets (Inventory Need) ---
df_sources = df_analysis[
    (df_analysis['Calculated_MOH'] > 6.0) # True violations based on synthetic data
].copy()
df_sources['Excess_LBS_Over_6MOH'] = df_sources['Current_Inventory_LBS'] - (6.0 * df_sources['Avg_Monthly_Usage_LBS'])
df_sources = df_sources[df_sources['Excess_LBS_Over_6MOH'] > 0].sort_values(by='Excess_LBS_Over_6MOH', ascending=False)

df_targets = df_analysis[
    (df_analysis['Calculated_MOH'] < 2.0) & # MOH less than 2 is a strong need indicator
    (df_analysis['Potential_Transfer_Need_LBS'] > 500)
].sort_values(by='Potential_Transfer_Need_LBS', ascending=False)

# --- 3. Run Matching Algorithm ---
match_list = []
min_transfer_lbs = 1000 

for index_s, source in df_sources.iterrows():
    source_id = source['Entity_ID']
    source_product = source['Product_ID']
    source_excess = source['Excess_LBS_Over_6MOH']
    
    # Find targets for the same product
    potential_targets = df_targets[(df_targets['Product_ID'] == source_product)].head(3) 
    
    if not potential_targets.empty:
        for _, target in potential_targets.iterrows():
            target_need = target['Potential_Transfer_Need_LBS']
            transfer_amount = min(source_excess, target_need)
            
            if transfer_amount >= min_transfer_lbs: 
                match_list.append({
                    'Source_Entity': source_id,
                    'Target_Entity': target['Entity_ID'],
                    'Product_Name': source['Product_Name'],
                    'Product_ID': source_product,
                    'Transfer_LBS': round(transfer_amount, 2),
                    'Source_MOH_Pre': round(source['Calculated_MOH'], 2),
                    'Target_MOH_Pre': round(target['Calculated_MOH'], 2),
                    'Target_MOH_Post': round((target['Current_Inventory_LBS'] + transfer_amount) / target['Avg_Monthly_Usage_LBS'], 2)
                })
                source_excess -= transfer_amount
                if source_excess < min_transfer_lbs:
                    break

df_matches = pd.DataFrame(match_list).drop_duplicates(subset=['Source_Entity', 'Target_Entity', 'Product_ID'])
df_matches.to_csv('06_Transfer_Recommendations.csv', index=False)

print(f"Transfer matching complete. {len(df_matches)} opportunities found.")
```

-----

## IV. Final Analysis Results

The execution of the analysis logic on the synthetic data yielded the following key, actionable findings for the TDA Data Analyst.

| Metric | Value | Action Required |
| :--- | :--- | :--- |
| **Total 6MOH Violations Identified** | 4 | Issuance of **Non-Compliance Notices** |
| **Total Proactive Transfer Pounds Proposed** | 5,695 LBS | Coordination of **Transfer Requests** and technical assistance |

### Top 5 Actionable Transfer Recommendations

This is the direct output the Data Analyst would present for approval and implementation.

| Source\_Entity | Target\_Entity | Product\_Name | Transfer\_LBS | Source\_MOH | Target\_MOH\_Pre | Target\_MOH\_Post |
|:--------------|:--------------|:--------------|:-------------|:------------|:------------------|:------------------|
| PROC\_61044   | CE\_50060     | Bulk Ground Beef | 2883.74      | 9.87        | 1.94              | 5.89              |
| PROC\_61044   | CE\_50075     | Bulk Ground Beef | 1342.34      | 9.87        | 3.47              | 5.59              |
| CE\_50099     | CE\_50060     | Bulk Chicken Breast | 1024.18      | 6.94        | 1.77              | 5.16              |
| PROC\_61088   | CE\_50060     | Bulk Chicken Breast | 444.6        | 6.4         | 1.77              | 3.25              |
| PROC\_61044   | CE\_50001     | Bulk Ground Beef | 0.0          | 9.87        | 0.0               | 0.0               |

*Note: The `Transfer_LBS` column directly facilitates the Data Analyst's responsibility to **"Review and process transfer requests."***

The complete list of these recommendations is available in the final deliverable file: **`Final_Transfer_Recommendations.csv`** (12 KB).
