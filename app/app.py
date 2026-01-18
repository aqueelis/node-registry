from flask import Flask, jsonify, render_template
import os
import socket
import requests
import hashlib

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "v1.0")
ECS_METADATA_URL = os.getenv("ECS_CONTAINER_METADATA_URI_V4")

def get_node_id():
    if not ECS_METADATA_URL:
        return f"Node-{socket.gethostname()}"

    try:
        resp = requests.get(f"{ECS_METADATA_URL}/task", timeout=5)
        resp.raise_for_status
        #hostname = socket.gethostname()
        # Create a stable numeric suffix from hostname
        #hash_value = int(hashlib.md5(hostname.encode()).hexdigest(), 16)
        #suffix = hash_value % 100  # Node-00 to Node-99
        task_arn = resp.json().get("TaskARN", "unknown")
        short_id = task_arn.split("/")[-1][:6]
        return f"Node-{short_id}"
    except Exception as e:
        return "Node-Unknown"
    

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/info")
def info():
    #node_id, hostname = get_node_id()
    return jsonify({
        "node": get_node_id(),
        "version": APP_VERSION,
        "hostname": socket.gethostname()
    })

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
