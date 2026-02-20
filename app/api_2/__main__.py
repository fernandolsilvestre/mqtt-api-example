from flask import Flask, jsonify, request

app = Flask(__name__)
@app.get("/")
def hello():
    return "Hello, World!"


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        request_data = request.get_json(silent=True)
    else:
        request_data = request.args.to_dict()

    print(f"Received request data: {request_data}")

    return jsonify({"message": "pong" if request_data and request_data.get("ask") == "ping" else "pong without ask ping"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)