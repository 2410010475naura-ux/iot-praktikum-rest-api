import paho.mqtt.client as mqtt
import json, time, random
from datetime import datetime

BROKER = "localhost"
TOPIC_SENSOR = "iot/sensor"
TOPIC_KONTROL = "iot/kontrol"

# Fungsi otomatis terpanggil saat broker MQTT terhubung
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        client.subscribe(TOPIC_KONTROL)
    else:
        print(f"Gagal terhubung ke broker, kode: {reason_code}")

# Fungsi otomatis terpanggil setiap ada perintah masuk dari dashboard/Node-RED
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"\n[PERINTAH DITERIMA] {msg.topic} -> {payload}\n")
    except Exception:
        print(f"\n[PERINTAH DITERIMA] {msg.payload.decode()}\n")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ESP32-Simulator")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_start()

print("ESP32 Simulator berjalan & mendengarkan perintah... Ctrl+C untuk stop")
try:
    while True:
        data = {
            "suhu": round(random.uniform(25, 32), 1),
            "kelembaban": round(random.uniform(55, 80), 1),
            "timestamp": datetime.now().isoformat()
        }
        client.publish(TOPIC_SENSOR, json.dumps(data))
        print(f"-> Publish: {data}")
        time.sleep(3)
except KeyboardInterrupt:
    print("Simulasi dihentikan.")
    client.loop_stop()
    client.disconnect()