from flask import Flask, jsonify, render_template
import os
import socket
import requests
import hashlib

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "v1.0")

def get_node_id():
    hostname = socket.gethostname()
    # Create a stable numeric suffix from hostname
    hash_value = int(hashlib.md5(hostname.encode()).hexdigest(), 16)
    suffix = hash_value % 100  # Node-00 to Node-99
    return f"Node-{suffix:02d}", hostname

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/info")
def info():
    node_id, hostname = get_node_id()
    return jsonify({
        "node": node_id,
        "version": APP_VERSION,
        "hostname": hostname
    })

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
