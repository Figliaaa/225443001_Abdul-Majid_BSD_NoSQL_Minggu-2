import paho.mqtt.client as mqtt
import time
import json
import random
from paho.mqtt.enums import CallbackAPIVersion

broker = "broker.hivemq.com"
port = 1883
topic = "pabrik/produksi"

client = mqtt.Client(CallbackAPIVersion.VERSION1)

print(f"Menghubungkan ke broker {broker}...")
client.connect(broker, port, 60)

print("Mulai mengirim data produksi (Tekan Ctrl+C untuk berhenti)...")
try:
    while True:
        data = {
            "batch": f"B-{random.randint(1000, 9999)}",
            "mesin": random.choice(["Mesin-A", "Mesin-B", "Mesin-C", "CNC-01"]),
            "jumlah": random.randint(100, 500),
            "reject": random.randint(0, 50)
        }
        
        payload = json.dumps(data)
        client.publish(topic, payload)
        
        print(f"Data terkirim -> {payload}")
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\nPublisher dihentikan.")
    client.disconnect()