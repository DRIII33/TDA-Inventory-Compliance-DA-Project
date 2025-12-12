CREATE OR REPLACE VIEW driiiportfolio.tda_compliance_data.tda_compliance_view AS
WITH Compliance_Metrics AS (
    SELECT
        Entity_ID, 
        Entity_Type, 
        Product_ID, 
        Product_Name, 
        Inventory_Date,
        Current_Inventory_LBS, 
        Avg_Monthly_Usage_LBS, 
        Calculated_MOH, 
        Best_By_Date,
        -- Calculate days until best-by date from the current date (assumed to be 2025-12-11 in the project context)
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
    -- Determine the appropriate intervention priority for the TDA Data Analyst
    CASE
        WHEN Days_Until_Best_By <= 180 AND Compliance_Status IN ('NON-COMPLIANT (6MOH VIOLATION)', 'HIGH-RISK (5-6 MOH)') 
             THEN 'IMMEDIATE ACTION: TRANSFER & COMPLIANCE REVIEW'
        WHEN Compliance_Status = 'NON-COMPLIANT (6MOH VIOLATION)' 
             THEN 'ACTION: NON-COMPLIANCE NOTICE & TRANSFER REQUIRED'
        WHEN Compliance_Status = 'HIGH-RISK (5-6 MOH)' 
             THEN 'ALERT: PROACTIVE TECHNICAL ASSISTANCE/TRANSFER OPPORTUNITY'
        ELSE 'MONITOR'
    END AS Intervention_Priority,
    -- Calculate the maximum inventory amount an entity can transfer or receive to hit exactly 6.0 MOH
    (6.0 - Calculated_MOH) * Avg_Monthly_Usage_LBS AS Potential_Transfer_Need_LBS
FROM
    Compliance_Metrics;
