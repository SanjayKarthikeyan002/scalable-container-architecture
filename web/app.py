from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# In docker-compose / on EC2, "backend" resolves via the shared Docker network.
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:5001")


@app.route("/")
def home():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=2)
        backend_status = r.json()
    except Exception as e:
        backend_status = {"status": "unreachable", "error": str(e)}

    return jsonify(
        {
            "service": "web",
            "message": "Hello from the web tier!",
            "backend": backend_status,
        }
    )


@app.route("/health")
def health():
    """This is the path the ALB health check will hit."""
    return jsonify({"status": "healthy", "service": "web"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
