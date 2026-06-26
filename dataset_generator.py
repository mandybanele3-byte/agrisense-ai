import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

rows = 1000

farms = ["Farm A","Farm B","Green Valley","Desert Bloom"]
locations = ["Dubai","Abu Dhabi","Al Ain","Sharjah","RAK","Fujairah"]
crops = ["Date Palm","Tomato","Cucumber","Lettuce","Pepper","Strawberry","Corn"]

data = []
start = datetime(2025,1,1)

for i in range(rows):
    dt = start + timedelta(hours=i*6)

    temp = np.random.randint(28,48)
    humidity = np.random.randint(30,90)
    soil = np.random.randint(10,80)
    rain = np.random.randint(0,10)
    wind = np.random.randint(5,30)
    uv = np.random.randint(6,12)

    ph = round(np.random.uniform(5.5,8.5),2)
    N = np.random.randint(10,60)
    P = np.random.randint(10,60)
    K = np.random.randint(10,60)

    if soil < 30 and temp > 38:
        irrigation = "High"
        duration = np.random.randint(30,60)
    elif soil < 50:
        irrigation = "Medium"
        duration = np.random.randint(15,30)
    else:
        irrigation = "Low"
        duration = np.random.randint(5,15)

    if rain > 5:
        irrigation = "Low"

    disease = "High" if humidity > 75 else "Medium" if humidity > 50 else "Low"
    heat = "High" if temp > 42 else "Medium" if temp > 35 else "Low"

    confidence = np.random.randint(90,99)
    water_saved = np.random.randint(50,300)
    health = np.random.randint(60,100)

    alert = irrigation == "High"

    data.append([
        dt.date(),
        dt.time(),
        random.choice(farms),
        random.choice(locations),
        random.choice(crops),
        soil,
        temp,
        humidity,
        ph,
        N,
        P,
        K,
        rain,
        wind,
        uv,
        irrigation,
        duration,
        confidence,
        water_saved,
        health,
        disease,
        heat,
        alert
    ])

columns = [
    "Date","Time","Farm","Location","Crop",
    "SoilMoisture","Temperature","Humidity","pH","Nitrogen","Phosphorus","Potassium",
    "Rainfall","WindSpeed","UV",
    "Irrigation","WaterDuration","AI_Confidence",
    "WaterSaved","PlantHealth","DiseaseRisk","HeatStress","Alert"
]

df = pd.DataFrame(data, columns=columns)

df.to_excel("agrisense_1000_records.xlsx", index=False)

print("✅ Dataset created successfully!")