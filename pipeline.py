import duckdb

# 1. Connect and Wipe (Starting fresh ensures no old data types interfere)
con = duckdb.connect('aero_ops.db')

con.execute("""
    -- BRONZE: Load Raw
    CREATE OR REPLACE TABLE bronze_flights AS 
    SELECT * FROM read_csv_auto('flight_telemetry.csv');
            
""")

con.execute("""
    CREATE OR REPLACE TABLE silver_flights AS
    SELECT 
        tail_number,
        -- Using json_extract ensures we get the raw numeric value
        CAST(json_extract(sensor_json, '$.vibration_level') AS DOUBLE) AS vibration,
        CAST(json_extract(sensor_json, '$.fuel_burn_rate') AS DOUBLE) AS fuel_burn
    FROM bronze_flights
""")

# ---------------------------------------------------------
# GOLD LAYER: Double-Checking the Math
# ---------------------------------------------------------
con.execute("""
    CREATE OR REPLACE TABLE gold_executive_dashboard AS
    SELECT 
        tail_number,
        ROUND(AVG(vibration), 2) AS "Avg Vibration",
        COUNT(CASE WHEN vibration > 0.7 THEN 1 END) AS "Risk Events",
        -- We multiply by 0.1500 to force the decimal precision
        ROUND(SUM(CASE 
            WHEN vibration > 0.7 THEN (fuel_burn * 0.1500) 
            ELSE 0 
        END), 0) AS "Wasted Fuel (Gal)"
    FROM silver_flights
    GROUP BY tail_number
    ORDER BY "Wasted Fuel (Gal)" DESC
""")

# 2. THE REVEAL
print("\n--- EXECUTIVE DASHBOARD: FUEL WASTE BY AIRCRAFT ---")
print(con.execute("SELECT * FROM gold_executive_dashboard").df())
con.close()
