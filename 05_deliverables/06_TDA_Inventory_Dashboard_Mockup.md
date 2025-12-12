---

# TDA Inventory Compliance and Transfer Optimization Dashboard

This dashboard provides a comprehensive, two-page analytical tool for proactive inventory management.

* **Page 1** identifies and prioritizes compliance risks (6MOH violations and spoilage threats).
* **Page 2** validates the success of data-driven intervention by measuring total pounds transferred and the resulting inventory health gain for recipient entities.

---

## 📄 Page 1: Compliance & Risk Monitoring

### **A. Executive Summary Scorecards**

#### **Chart 1: % Non-Compliant**

* **Value:** 28.57% (Example)
* **Insight:** Percentage of unique TDA entities currently failing the 6MOH standard.
* **Formatting:** Red if ≥ 10%.

#### **Chart 2: Total At-Risk LBS**

* **Value:** 85,250.99 LBS (Example)
* **Insight:** Quantifies total excess inventory exceeding the 6-month hold limit.
* **Filter:** `Potential_Transfer_Need_LBS < 0`
* **Formatting:** Orange text.

---

### **B. Risk Prioritization and Source Identification**

#### **Chart 3: Spoilage & Risk Heatmap**

* **Dimensions:**

  * `Entity_ID`
  * `Product_Name`
  * `Calculated_MOH` (Number)
  * `Days_Until_Best_By` (Number)
* **Sorting:** `Days_Until_Best_By` ascending
* **Conditional Formatting:**

  * `Days_Until_Best_By ≤ 180` → Background **red**
  * `Intervention_Priority` → Color-coded (**red/orange/yellow**)
* **Insight:** Operational watchlist for immediate analyst action.

#### **Chart 4: Violation Count by Product**

* **Dimension:** `Product_Name`
* **Metric:** Count of 6MOH violations
* **Filter:** `Compliance_Status = 'NON-COMPLIANT (6MOH VIOLATION)'`
* **Sorting:** Descending by count
* **Insight:** Identifies commodities requiring urgent systemic action.

---

## 📄 Page 2: Intervention & Transfer Analysis

### **C. Intervention Success Metrics**

#### **Chart 5: Total Pounds Transferred**

* **Value:** 5,104.48 LBS (Example)
* **Insight:** Total volume of excess inventory successfully reallocated.

#### **Chart 6: Top 5 Potential Transfer Needs (Recipients)**

* **Filter:** `Calculated_MOH < 5.0`
* **Sorting:** `Potential_Transfer_Need_LBS` descending
* **Limit:** Top 5
* **Insight:** Identifies best recipients able to absorb inventory effectively.

---

### **D. Impact Validation**

#### **Chart 7: Average MOH Improvement (Intervention Validation Table)**

* **Data Source:**
  `tda_compliance_view LEFT JOIN 06_Transfer_Recommendations.csv`

* **Dimensions:**

  * `Product_Name`
  * `Target_Entity`

* **Metrics:**

  * `Source_MOH_Pre (AVG)`
  * `Target_MOH_Post (AVG)`
  * `Transfer_LBS (SUM)`
  * `Recipient_MOH_Gain` (Calculated)

* **Calculated Field:**

  ```
  Recipient_MOH_Gain = AVG(Target_MOH_Post) - AVG(Calculated_MOH)
  ```

* **Filters & Formatting:**

  * `Transfer_LBS IS NOT NULL`
  * Sort by `Transfer_LBS` descending
  * MOH values formatted as numbers (ratios)

* **Insight:**
  Validates the effectiveness of transfer recommendations by measuring MOH improvement for recipients.

---

