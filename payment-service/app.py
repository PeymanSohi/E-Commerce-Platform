from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("payment-service")

@app.route('/pay', methods=['POST'])
def process_payment():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        order_id = data.get("order_id")
        amount = data.get("amount")

        logger.info(f"[payment-service] Processing payment: user={user_id}, order={order_id}, amount={amount}")

        # Simulate payment success
        return jsonify({
            "status": "success",
            "message": f"Payment of ${amount} for order {order_id} processed."
        }), 200
    except Exception as e:
        logger.error(f"[payment-service] Payment error: {str(e)}")
        return jsonify({"status": "error", "message": "Payment failed"}), 500

@app.route('/health')
def health():
    return {"status": "payment-service is healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
