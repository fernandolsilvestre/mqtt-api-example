import json
import paho.mqtt.client as mqtt
import requests

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

REQUEST_TOPIC = "api/ping/request"
RESPONSE_TOPIC = "api/ping/response"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with reason code {reason_code}")
    client.subscribe(REQUEST_TOPIC, qos=1)

client.on_connect = on_connect

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        payload_json = json.loads(payload)
    except json.JSONDecodeError:
        payload_json = {"raw": payload}

    try:
        response = requests.post("http://localhost:5001/ping", json=payload_json, timeout=5)
        try:
            upstream_message = response.json().get('message', 'No message in response')
        except requests.exceptions.JSONDecodeError:
            upstream_message = {
                "status_code": response.status_code,
                "text": response.text,
            }
    except requests.RequestException as exc:
        upstream_message = {
            "error": str(exc),
        }

    response_payload = {"message": upstream_message, "received": payload_json}

    client.publish(RESPONSE_TOPIC, json.dumps(response_payload), qos=1, retain=False)
    print(f"request: {payload_json} -> response: {response_payload}")

client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()