
import os
import yaml
import logging

logger = logging.getLogger(__name__)

def load_config():
    with open("../../shared/config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()

API_TOKEN = os.environ.get(config["api"]["auth_token_env"])
MAX_RETRIES = config["api"]["max_retries"]

class PaymentProcessor:

    def __init__(self):
        self.processed_payments = []

    def process_payment(self, order_id, amount, payment_method="credit_card"):
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        if amount > 10000:
            logger.warning(f"Large payment detected: ${amount} for order {order_id}")

        payment = {
            "payment_id": len(self.processed_payments) + 1,
            "order_id": order_id,
            "amount": amount,
            "method": payment_method,
            "status": "completed"
        }

        self.processed_payments.append(payment)
        return payment

    def refund_payment(self, payment_id):
        for payment in self.processed_payments:
            if payment["payment_id"] == payment_id:
                payment["status"] = "refunded"
                return payment
        return None

