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
