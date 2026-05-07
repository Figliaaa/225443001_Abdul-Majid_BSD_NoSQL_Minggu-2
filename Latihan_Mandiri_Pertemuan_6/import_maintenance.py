import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["latihan6"]
collection = db["maintenance"]

print("Membaca file maintenance.csv...")
df = pd.read_csv("maintenance.csv")

df["tanggal"] = pd.to_datetime(df["tanggal"])

data_records = df.to_dict(orient="records")

if data_records:
    collection.delete_many({}) 
    
    result = collection.insert_many(data_records)
    print(f"Berhasil menyisipkan {len(result.inserted_ids)} dokumen ke koleksi 'maintenance'.")