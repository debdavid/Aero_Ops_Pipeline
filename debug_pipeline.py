import duckdb

# Connect to the existing database
con = duckdb.connect('aero_ops.db')

print("\n--- 🔍 DIAGNOSTIC MODE: INSPECTING RAW DATA ---")

# We run a query that shows the RAW JSON text next to what we THINK we are extracting
debug_query = """
    SELECT 
        tail_number, 
        -- 1. Show me the raw text blob (so we can check spelling)
        sensor_json AS raw_json_blob,
        
        -- 2. Show me what the extraction finds for Vibration (This works!)
        json_extract(sensor_json, '$.vibration_level') AS extract_vib,
        
        -- 3. Show me what the extraction finds for Fuel (This is failing!)
        json_extract(sensor_json, '$.fuel_burn_rate') AS extract_fuel
    FROM bronze_flights
    WHERE CAST(json_extract(sensor_json, '$.vibration_level') AS DOUBLE) > 0.7
    LIMIT 3
"""

# Run it and print the result
df = con.execute(debug_query).df()

# This setting ensures Python prints the full width of the JSON so we can read it
import pandas as pd
pd.set_option('display.max_colwidth', None)

print(df)