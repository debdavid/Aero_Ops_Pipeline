import pandas as pd
import json

# Load the raw CSV directly (bypassing DuckDB for a moment)
df = pd.read_csv('flight_telemetry.csv')

# Get the first row's JSON blob
first_json_blob = df['sensor_json'].iloc[0]

# Parse it nicely
data = json.loads(first_json_blob)

print("\n--- 🔍 RAW DATA INSPECTION ---")
print("Here are the EXACT keys inside your JSON file:")
for key, value in data.items():
    print(f"  • Key: '{key}'  -> Value: {value}")

print("\n-------------------------------")
