
import os
import yaml
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_config():
    with open("../../shared/config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()

API_TOKEN = os.environ.get(config["api"]["auth_token_env"])
DB_TIMEOUT = config["database"]["timeout_seconds"]

orders_db = []

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data.get("customer_id"):
        return jsonify({"error": "customer_id is required"}), 400
    if not data.get("items") or len(data["items"]) == 0:
        return jsonify({"error": "At least one item is required"}), 400

    total = sum(item["price"] * item["quantity"] for item in data["items"])

    order = {
        "order_id": len(orders_db) + 1,
        "customer_id": data["customer_id"],
        "items": data["items"],
        "total": total,
        "status": "pending"
    }
    orders_db.append(order)

    return jsonify(order), 201

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    for order in orders_db:
        if order["order_id"] == order_id:
            return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "order-service"})

if __name__ == "__main__":
    app.run(port=5001)

