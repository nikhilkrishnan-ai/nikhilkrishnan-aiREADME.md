import pandas as pd

# NK's Forensic Data for Power BI
data = {
    'Time': ['2026-04-26 10:00', '2026-04-26 10:05', '2026-04-26 10:10', '2026-04-26 10:15'],
    'Lat': [24.4539, 24.4540, 28.6139, 24.4542],
    'Lon': [54.3773, 54.3774, 77.2090, 54.3776],
    'Velocity': [0, 15, 4500, 12],
    'Status': ['Normal', 'Normal', 'Jump to Delhi', 'Normal']
}

df = pd.DataFrame(data)
df.to_csv("forensic_final.csv", index=False)
print("✅ SUCCESS: forensic_final.csv created!")