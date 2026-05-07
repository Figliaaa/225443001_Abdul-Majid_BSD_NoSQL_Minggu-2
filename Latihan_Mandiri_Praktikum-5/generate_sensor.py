from pymongo import MongoClient
from datetime import datetime, timedelta
import random

NIM = "225443001"
client = MongoClient('mongodb://localhost:27017')
db = client[f'latihan5_{NIM}']

db.sensor_info.drop()
db.data_sensor.drop()

print(f"Menyiapkan database: latihan5_{NIM}...\n")
kategori_list = ["suhu", "tekanan", "kelembaban", "getaran", "arus"]
area_list = ["Utama", "Gudang", "Mesin A", "Mesin B", "Luar"]

info_docs = []
for i in range(1, 21):
    sensor_id = f"S{i:03d}"
    kategori = random.choice(kategori_list)
    area = random.choice(area_list)
    nama_sensor = f"Sensor {kategori.capitalize()} Area {area}"
    
    info_docs.append({
        "sensor_id": sensor_id,
        "nama_sensor": nama_sensor,
        "kategori_tetap": kategori 
    })

db.sensor_info.insert_many(info_docs)
print(f"[*] Koleksi 'sensor_info' selesai dibuat. Total: {db.sensor_info.count_documents({})} dokumen.")


docs = []
start_date = datetime.now() - timedelta(days=30)

for i in range(5000):
    sensor_terpilih = random.choice(info_docs)
    kategori = sensor_terpilih["kategori_tetap"]
    
    if kategori == "suhu":
        nilai = round(random.uniform(25.0, 95.0), 2)
    elif kategori == "kelembaban":
        nilai = round(random.uniform(40.0, 99.0), 2)
    else:
        nilai = round(random.uniform(10.0, 150.0), 2)

    timestamp = start_date + timedelta(minutes=random.randint(0, 60 * 24 * 30))
    
    doc = {
        "sensor_id": sensor_terpilih["sensor_id"],
        "nilai": nilai,
        "timestamp": timestamp,
        "category": kategori
    }
    
    docs.append(doc)
    
    if len(docs) >= 500:
        db.data_sensor.insert_many(docs)
        docs.clear()

if docs:
    db.data_sensor.insert_many(docs)

print(f"[*] Koleksi 'data_sensor' selesai dibuat. Total: {db.data_sensor.count_documents({})} dokumen.")
print("\nSemua data berhasil di-generate!")