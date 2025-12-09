import paho.mqtt.client as mqtt
import time
import json

MQTT_HOST = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "test/arduino_asistencia"

client = mqtt.Client()

client.connect(MQTT_HOST, MQTT_PORT)

'''
payload = 'agjhkjg'
client.publish(MQTT_TOPIC, payload)
print(f"Mensaje enviado: {payload}")
'''
tarjetas = ["73BAE212", "B30E361C", "A1B2C3D4", "E1B443U4", "Z1B2C3B0", "D4E5F6G7", "63D7CD11"]

for i in tarjetas:
    '''
    payload = {
        "id_usuario": f"user_{i}",
        "timestamp": time.time(),
        "evento": "entrada"
    }
    client.publish(MQTT_TOPIC, json.dumps(payload))
    '''
    payload = i
    client.publish(MQTT_TOPIC, payload)
    print(f"Mensaje enviado: {payload}")
    time.sleep(2)  # Espera entre mensajes

client.disconnect()