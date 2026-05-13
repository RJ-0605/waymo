from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import random
import time

app = Flask(__name__)

payment_requests = Counter(
    "payment_requests_total",
    "Total payment requests",
    ["status"]
)

payment_latency = Histogram(
    "payment_request_duration_seconds",
    "Payment request latency"
)

@app.route("/pay")
@payment_latency.time()
def pay():

    processing_time = random.uniform(0.1, 0.5)
    time.sleep(processing_time)

    if random.random() > 0.2:
        payment_requests.labels(status="success").inc()

        return jsonify({
            "status": "success",
            "latency": processing_time
        })

    payment_requests.labels(status="failed").inc()

    return jsonify({
        "status": "failed",
        "latency": processing_time
    }), 500


@app.route("/metrics")
def metrics():
    return generate_latest()


@app.route("/")
def home():
    return "Payment API Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)