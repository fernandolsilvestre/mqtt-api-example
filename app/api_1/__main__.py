from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import json
from threading import Event

app = Flask(__name__)

REQUEST_TOPIC = "api/ping/request"
RESPONSE_TOPIC = "api/ping/response"

response_event = Event()
message = None

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with reason code {reason_code}")
    client.subscribe(RESPONSE_TOPIC, qos=1)

def on_message(client, userdata, msg):
    global message
    payload = msg.payload.decode()
    try:
        payload_json = json.loads(payload)
    except json.JSONDecodeError:
        payload_json = {"raw": payload}

    message = payload_json
    response_event.set()

    print(f"Topic: {msg.topic}, Message: {payload}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_start()

@app.get('/ping')
def ping():
    global message

    message = None
    response_event.clear()

    client.publish(REQUEST_TOPIC, payload=json.dumps({
        "ask": "ping"
    }), qos=1, retain=False)

    if not response_event.wait(timeout=3):
        return jsonify({"error": "timeout waiting MQTT response"}), 504

    return jsonify({"response": message})

if __name__ == "__main__":
    app.run(debug=True)