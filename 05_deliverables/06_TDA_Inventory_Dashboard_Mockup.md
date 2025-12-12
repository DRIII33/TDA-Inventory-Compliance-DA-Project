This document serves as the **`06_TDA_Inventory_Dashboard_Mockup.pdf`**, providing a detailed, structured blueprint for the two-page Looker Studio dashboard. It incorporates all final corrections for logic, filtering, and formatting to ensure the dashboard aligns perfectly with the TDA project objectives.

---

## **06\_TDA\_Inventory\_Dashboard\_Mockup.pdf**

### **TDA Inventory Compliance and Transfer Optimization Dashboard**

This dashboard provides a comprehensive, two-page analytical tool for proactive inventory management. The first page focuses on identifying and prioritizing compliance risks (6MOH violations and spoilage threats), while the second page validates the success of data-driven intervention by measuring the total pounds transferred and the resulting inventory health gain for recipient entities. It transforms raw inventory data into actionable insights, enabling TDA analysts to quickly triage urgent situations and efficiently optimize food distribution.

---

## **Page 1: Compliance & Risk Monitoring**

*(Focus: Identifying the Scope and Urgency of the Problem)*

### **A. Executive Summary Scorecards (Top Row)**

| **Chart 1: % Non-Compliant** | **Chart 2: Total At-Risk LBS** |
| :--- | :--- |
| **Value:** 28.57% (Example) | **Value:** 85,250.99 LBS (Example) |
| **Insight:** High-level KPI showing the percentage of unique TDA entities currently failing the 6MOH standard. | **Insight:** Quantifies the total excess inventory that exceeds the 6-month hold limit across all non-compliant sources. |
| **Formatting:** **Color-Coded Red** if $\ge 10\%$. **Filter:** None. | **Formatting:** **Orange** text. **Chart Filter:** $\text{Potential\_Transfer\_Need\_LBS} < 0$. |

### **B. Risk Prioritization and Source Identification**

#### **Chart 3: Spoilage & Risk Heatmap (Operational Watchlist)**

* **Chart Type:** Table with Conditional Formatting.
* **Dimensions:** $\text{Entity\_ID}$, $\text{Product\_Name}$, $\text{Calculated\_MOH}$ (Number), $\text{Days\_Until\_Best\_By}$ (Number).
* **Key Filtering/Sorting:**
    * **Sorting:** Primary sort by $\text{Days\_Until\_Best\_By}$ **Ascending** (shortest shelf life first).
    * **Conditional Formatting Rule 1:** $\text{Days\_Until\_Best\_By} \le 180$ days $\rightarrow$ **Cell Background RED**.
    * **Conditional Formatting Rule 2:** $\text{Intervention\_Priority}$ column color-coded by urgency (RED, ORANGE, YELLOW).
* **Insight:** A prioritized operational watchlist designed for immediate analyst action, combining MOH risk with time-sensitive spoilage threats.

#### **Chart 4: Violation Count by Product (Commodity Risk)**

* **Chart Type:** Horizontal Bar Chart.
* **Dimension:** $\text{Product\_Name}$.
* **Metric:** Count of records (representing 6MOH violations).
* **Key Filtering/Sorting:**
    * **Chart Filter:** $\text{Compliance\_Status}$ **EQUAL TO** 'NON-COMPLIANT (6MOH VIOLATION)'.
    * **Sorting:** Descending by Count of records.
* **Insight:** Identifies the USDA commodity types that require the most urgent systemic attention and transfer coordination due to high violation frequency.

---

## **Page 2: Intervention & Transfer Analysis**

*(Focus: Validating the Solution and Identifying Recipients)*

### **C. Intervention Success Metrics (Top Row)**

| **Chart 5: Total Pounds Transferred** | **Chart 6: Top 5 Potential Transfer Needs (Recipients)** |
| :--- | :--- |
| **Value:** 5,104.48 LBS (Example) | **Chart Type:** Vertical Bar Chart. |
| **Insight:** Measures the total physical volume of excess inventory successfully reallocated due to the data-driven intervention. | **Insight:** Identifies the top five compliant entities that have the largest capacity to efficiently absorb inventory (up to $5.0$ MOH). |
| **Formatting:** **Green** text to signify successful waste prevention. | **Filter:** $\text{Calculated\_MOH}$ **Less than** $5.0$. **Sorting:** $\text{Potential\_Transfer\_Need\_LBS}$ Descending. **Limit:** Set to **5** rows/bars. |

### **D. Impact Validation**

#### **Chart 7: Average MOH Improvement (Intervention Validation Table)**

* **Data Source:** Blended Data (`tda_compliance_view` LEFT JOIN `06_Transfer_Recommendations.csv`).
* **Dimensions:** $\text{Product\_Name}$, $\text{Target\_Entity}$.
* **Metrics:** $\text{Source\_MOH\_Pre}$ (AVG), $\text{Target\_MOH\_Post}$ (AVG), $\text{Transfer\_LBS}$ (SUM), **`Recipient MOH Gain`** (Calculated Field).
* **Calculated Field (Correction Applied):** $\text{Recipient MOH Gain} = \text{AVG}(\text{Target\_MOH\_Post}) - \text{AVG}(\text{Calculated\_MOH})$.
* **Key Filtering/Sorting:**
    * **Chart Filter:** $\text{Transfer\_LBS}$ **Is Not Null** (Only show impacted entities).
    * **Sorting:** $\text{Transfer\_LBS}$ **Descending** (Prioritize largest transfers).
    * **Formatting:** $\text{Source\_MOH\_Pre}$ and $\text{Target\_MOH\_Post}$ formatted as **Number** (MOH is a ratio, not a percentage).
* **Insight:** Provides empirical proof that the transfer process successfully increased the recipient's inventory health (positive `Recipient MOH Gain`), validating the analyst's transfer recommendations.
