import paho.mqtt.client as mqtt
import json
from datetime import datetime
from pymongo import MongoClient

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["latihan6"]
col = db["produksi_mqtt"]

broker = "broker.hivemq.com"
port = 1883
topic = "pabrik/produksi"

def on_connect(client, userdata, flags, rc):
    print(f"Terhubung ke MQTT Broker dengan kode hasil: {rc}")
    client.subscribe(topic)
    print(f"Berlangganan pada topik: {topic}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    data = json.loads(payload)
    
    data["timestamp"] = datetime.now()
    
    jumlah = data.get("jumlah", 0)
    reject = data.get("reject", 0)
    
    if jumlah > 0:
        reject_rate = (reject / jumlah) * 100
        
        if reject_rate > 5.0:
            print(f"\n[PERINGATAN] Reject Rate tinggi! ({reject_rate:.2f}%) pada {data['mesin']}")
            data["peringatan"] = True
    
    col.insert_one(data)
    
    data_to_print = data.copy()
    data_to_print.pop('_id', None)
    print(f"Tersimpan di DB: {data_to_print}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"Menghubungkan ke broker {broker}...")
client.connect(broker, port, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nSubscriber dihentikan.")
    client.disconnect()