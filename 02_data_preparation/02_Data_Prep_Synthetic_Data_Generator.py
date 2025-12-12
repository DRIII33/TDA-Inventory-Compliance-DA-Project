import pandas as pd
import numpy as np
from datetime import date, timedelta
import random

# --- Configuration ---
PROJECT_NAME = "TDA-Inventory-Compliance-DA-Project"
FILE_NAME = "Inventory_Usage_Synthetic_Data.csv"
TODAY = date(2025, 12, 11) # Set to the context date for realistic MOH calculation
START_DATE = date(2025, 10, 31)

# List of Entity IDs and Product Details
entity_data = {
    'CE_50012': 'Contracting Entity', 'CE_50035': 'Contracting Entity',
    'PROC_61044': 'Processor', 'PROC_61088': 'Processor',
    'CE_50099': 'Contracting Entity', 'PROC_61022': 'Processor',
    'CE_50060': 'Contracting Entity', 'PROC_61010': 'Processor',
    'CE_50075': 'Contracting Entity', 'CE_50001': 'Contracting Entity'
}

product_data = {
    'US_CHICKEN_BR_BULK': {'name': 'Bulk Chicken Breast', 'max_moh': 7},
    'US_BEEF_GR_BULK': {'name': 'Bulk Ground Beef', 'max_moh': 7},
    'US_PEACHES_CANNED': {'name': 'Canned Sliced Peaches', 'max_moh': 12},
    'US_CHEESE_SHRED': {'name': 'Shredded Cheddar Cheese', 'max_moh': 6},
    'US_RICE_BAG': {'name': 'Bagged Long Grain Rice', 'max_moh': 18}
}

# --- Data Generation Function ---
def generate_inventory_data():
    data = []
    report_id_counter = 1
    
    # Generate data for a single month (e.g., October 2025 MPR submission)
    inventory_date = START_DATE
    
    for entity_id, entity_type in entity_data.items():
        for product_id, details in product_data.items():
            
            # Scenario 1: Intentional Compliance Risk (High MOH)
            if entity_id in ['PROC_61044', 'CE_50099'] and product_id in ['US_BEEF_GR_BULK', 'US_CHICKEN_BR_BULK']:
                # Set Inventory_LBS to be significantly higher than usage (e.g., 7-9 MOH)
                avg_usage = random.uniform(1500, 3000) 
                inventory_lbs = avg_usage * random.uniform(7.0, 9.0) # **NON-COMPLIANCE RISK**
                best_by_days = random.randint(90, 150) # Closer to expiration
            
            # Scenario 2: Normal Compliance (Low MOH)
            else:
                avg_usage = random.uniform(500, 4000)
                inventory_lbs = avg_usage * random.uniform(2.0, 5.5) # Compliance
                best_by_days = random.randint(180, 500)
            
            # Scenario 3: Transfer Opportunity (CE with low MOH needs product from a high MOH Processor)
            if entity_id == 'CE_50001' and product_id == 'US_CHICKEN_BR_BULK':
                 # Set low inventory, indicating need
                 avg_usage = 3500
                 inventory_lbs = 500 # Very low MOH, ideal transfer target
            
            
            best_by_date = (inventory_date + timedelta(days=best_by_days)).strftime('%Y-%m-%d')
            
            # Calculate Months of Hold (MOH)
            calculated_moh = inventory_lbs / avg_usage if avg_usage > 0 else 0
            
            data.append({
                'Report_ID': f'MPR_TDA_{inventory_date.strftime("%m%Y")}_{report_id_counter:04}',
                'Entity_ID': entity_id,
                'Entity_Type': entity_type,
                'Product_ID': product_id,
                'Product_Name': details['name'],
                'Inventory_Date': inventory_date.strftime('%Y-%m-%d'),
                'Current_Inventory_LBS': round(inventory_lbs, 2),
                'Avg_Monthly_Usage_LBS': round(avg_usage, 2),
                'Best_By_Date': best_by_date,
                'Calculated_MOH': round(calculated_moh, 2)
            })
            report_id_counter += 1

    return pd.DataFrame(data)

# Generate and save the data
df_inventory = generate_inventory_data()
df_inventory.to_csv(FILE_NAME, index=False)

print(f"✅ Synthetic data generated and saved as: {FILE_NAME}")
print(df_inventory.head())
