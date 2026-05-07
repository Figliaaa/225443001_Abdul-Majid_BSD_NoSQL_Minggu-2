from pymongo import MongoClient
from datetime import datetime, timedelta
import random

KELOMPOK = "kelompok_2"
client = MongoClient('mongodb://localhost:27017')
db = client[f'tugas5_{KELOMPOK}']
db.inspeksi.drop()
db.target_kualitas.drop()

mesin_list = [f"M{i:02d}" for i in range(1, 11)]
batch_ids = [f"B{str(i).zfill(4)}" for i in range(1, 2001)]
inspektor_list = ["Abdul", "Arlisya", "Farrel", "Rakandya", "Shiva"]
jenis_cacat_options = ["gores", "retak", "bengkok", "warna", "dimensi", "pori"]

docs = []
start_date = datetime(2026, 4, 1, 6, 0)
for i in range(1000):
    batch = random.choice(batch_ids)
    mesin = random.choice(mesin_list)
    tanggal = start_date + timedelta(minutes=random.randint(0, 60*24*90))
    shift = 1 if tanggal.hour < 14 else (2 if tanggal.hour < 22 else 3)
    jumlah = random.randint(100, 500)
    reject = int(jumlah * random.uniform(0, 0.10))  
    jenis = random.sample(jenis_cacat_options, k=random.randint(1, 3))
    doc = {
        "batch_id": batch,
        "mesin": mesin,
        "tanggal": tanggal,
        "shift": shift,
        "inspektor": random.choice(inspektor_list),
        "jumlah_diperiksa": jumlah,
        "cacat_ditemukan": reject,
        "jenis_cacat": jenis
    }
    docs.append(doc)
    if len(docs) >= 500:
        db.inspeksi.insert_many(docs)
        docs.clear()
if docs:
    db.inspeksi.insert_many(docs)

print("Data inspeksi selesai. Total:", db.inspeksi.count_documents({}))

targets = []
for i in range(1, 2001):
    batch = f"B{str(i).zfill(4)}"
    target_cacat = random.randint(1, 15)
    targets.append({"batch_id": batch, "target_maks_cacat": target_cacat})
    if len(targets) >= 500:
        db.target_kualitas.insert_many(targets)
        targets.clear()
if targets:
    db.target_kualitas.insert_many(targets)

print("Data target kualitas selesai. Total:", db.target_kualitas.count_documents({}))