from flask import Flask, jsonify
import datetime

app = Flask(__name__)


@app.route("/health")
def health():
    """Used by the web tier and by any monitoring to check this service is alive."""
    return jsonify({"status": "healthy", "service": "backend"}), 200


@app.route("/api/data")
def data():
    """A tiny 'real' endpoint so this isn't just a health check with extra steps."""
    return jsonify(
        {
            "service": "backend",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "message": "data from backend tier",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
