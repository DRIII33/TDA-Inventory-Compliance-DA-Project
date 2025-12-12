## Mitigating Spoilage Risk via 6MOH Compliance

**01_Business_Understanding_Problem_Statement.pdf: Mitigating Spoilage Risk via 6MOH Compliance**

### 1. Introduction
The Technical Assistance (TDA) program is responsible for the efficient management and distribution of USDA Foods to local contracting entities (CEs) and processors. A critical Key Performance Indicator (KPI) for the program is inventory management, specifically preventing the accumulation of excess stock that risks spoilage. This document formally outlines the problem driven by the 6 Months of Hold (6MOH) compliance rule and defines the scope of a data project designed to solve it.

### 2. The 6MOH Compliance Mandate
The 6MOH rule requires that any participating entity must maintain a level of inventory such that their Current Inventory (LBS) divided by their Average Monthly Usage (LBS) is less than 6.0.

**Calculated MOH** = (Current Inventory LBS) / (Avg. Monthly Usage LBS) ≤ 6.0

Any inventory classified with an **MOH** greater than or equal to 6.0 is deemed Non-Compliant and represents an immediate spoilage risk and program inefficiency.

### 3. Current Pain Points for the TDA Analyst
The current process for managing this risk is manual and reactive:

* **Late Detection:** Violations are often identified only after inventory reports are submitted, leaving little time before best-by dates are reached.
* **Ineffective Triage:** There is no standard method to prioritize which non-compliant records pose the highest combined risk (high **MOH** AND approaching expiration).
* **Suboptimal Transfers:** Transfer decisions rely on communication and availability, failing to leverage data on the recipient's true capacity to absorb inventory without becoming high-risk themselves (**MOH** < 5.0).

### 4. Project Scope and Objectives
| Objective | Deliverable | Success Criteria |
| :--- | :--- | :--- |
| A. Centralize Logic | Creation of the BigQuery View `tda_compliance_view`. | All compliance logic (**Compliance_Status**, **Intervention_Priority**) is calculated and centralized in the database, eliminating Looker Studio calculated fields. |
| B. Quantify Risk & Need | Dashboard Page 1: Compliance & Risk Monitoring. | Visualization of total pounds at risk (**Total At-Risk LBS**) and clear prioritization of entities facing imminent spoilage. |
| C. Optimize Intervention | Python Matching Script and Dashboard Page 2: Transfer Impact. | Identification of **Top 5** Recipients (**MOH** < 5.0 pool) and calculation of a positive **Recipient MOH Gain** for successful transfers. |

### 5. Defined Risk Tiers (Implemented in `tda_compliance_view`)
| MOH Range | Compliance Status | Intervention Priority |
| :--- | :--- | :--- |
| **MOH** ≥ 6.0 | NON-COMPLIANT (6MOH VIOLATION) | ACTION: Non-Compliance Notice & Transfer Required |
| 5.0 ≤ **MOH** < 6.0 | HIGH-RISK (5-6 MOH) | ALERT: Proactive Technical Assistance/Transfer Opportunity |
| **MOH** < 5.0 | COMPLIANT | MONITOR (Primary pool for recipient transfers) |

***
