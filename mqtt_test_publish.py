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

for i in range(5):
    '''
    payload = {
        "id_usuario": f"user_{i}",
        "timestamp": time.time(),
        "evento": "entrada"
    }
    client.publish(MQTT_TOPIC, json.dumps(payload))
    '''
    payload = f"id_usuario{i}"
    client.publish(MQTT_TOPIC, payload)
    print(f"Mensaje enviado: {payload}")
    time.sleep(2)  # Espera entre mensajes

client.disconnect()