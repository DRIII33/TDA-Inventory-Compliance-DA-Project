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
