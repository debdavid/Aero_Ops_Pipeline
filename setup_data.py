import pandas as pd
import random
import json
from datetime import datetime

# 1. MAINTENANCE SCHEDULE
aircraft = ['VH-XZA', 'VH-XZB', 'VH-XZC', 'VH-XZD']
data_rows = []

print("🏭 Generating 500 flights with REALISTIC PHYSICS...")

for i in range(500):
    date = datetime(2026, 1, random.randint(1, 30))
    plane = random.choice(aircraft)
    
    # 2. Set Vibration Profile
    # VH-XZD is the "Lemon" (High Vibration)
    if plane == 'VH-XZD':
        vibration = round(random.uniform(0.7, 0.9), 2)
    else:
        vibration = round(random.uniform(0.3, 0.5), 2)

    # 3. THE PHYSICS ENGINE UPGRADE 🚀
    # Old Way: Random number (2200-2800)
    # New Way: Fuel Burn is directly caused by Vibration efficiency loss
    # Base burn is 2000. Every 0.1 increase in vibration adds ~100 lbs of drag/waste.
    base_burn = 2200
    drag_penalty = (vibration * 800) 
    random_noise = random.randint(-50, 50) # Tiny variation for realism
    
    final_fuel = int(base_burn + drag_penalty + random_noise)

    sensor_data = {
        "engine_temp": random.randint(700, 980),
        "vibration_level": vibration,
        "fuel_burn_rate": final_fuel 
    }

    # 4. Pack it
    data_rows.append({
        'flight_id': f"FL{random.randint(1000, 9999)}",
        'flight_date': date.strftime('%Y-%m-%d'),
        'tail_number': plane,
        'sensor_json': json.dumps(sensor_data)
    })

# 5. Save the file
df_flights = pd.DataFrame(data_rows)
df_flights.to_csv('flight_telemetry.csv', index=False)

print(f"✅ Success! Generated physics-accurate telemetry.")
