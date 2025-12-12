-- DELIVERABLE: 03_Data_Prep_ETL_BigQuery.sql
-- DESCRIPTION: SQL script to create the table and perform initial data inspection in Google BigQuery.

-- 1. Create the Dataset (Run once if it doesn't exist)
-- Note: This step is usually done via the BigQuery UI, but included for completeness.
-- CREATE SCHEMA driiiportfolio.tda_compliance_data;

-- 2. Create the Inventory MPR Table (Assuming manual or GCS load)
-- This query is a placeholder for the schema definition used for the CSV load.
/*
CREATE TABLE driiiportfolio.tda_compliance_data.inventory_mpr (
    Report_ID STRING,
    Entity_ID STRING,
    Entity_Type STRING,
    Product_ID STRING,
    Product_Name STRING,
    Inventory_Date DATE,
    Current_Inventory_LBS FLOAT64,
    Avg_Monthly_Usage_LBS FLOAT64,
    Best_By_Date DATE,
    Calculated_MOH FLOAT64
);
*/

-- 3. Data Validation and Inspection Query (Sanity Check)
SELECT
    Entity_Type,
    COUNT(DISTINCT Entity_ID) AS Total_Entities,
    COUNT(Product_ID) AS Total_Inventory_Records,
    SUM(Current_Inventory_LBS) AS Total_Inventory_LBS,
    MIN(Inventory_Date) AS Oldest_Report_Date
FROM
    `driiiportfolio.tda_compliance_data.inventory_mpr`
GROUP BY 1
ORDER BY Total_Entities DESC;
