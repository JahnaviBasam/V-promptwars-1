from flask import Flask, request, jsonify
import uuid
import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# In-memory mock database (Replaces Firebase if offline)
firebase_mock_state = {
    "gates": {
        "gate_a": {"density": 30.0, "active_vouchers": 0},
        "gate_b": {"density": 20.0, "active_vouchers": 0}
    },
    "queues": []
}

@app.route('/')
def serve_index():
    """Serves the main frontend dashboard."""
    return app.send_static_file('index.html')

@app.route('/api/state', methods=['GET'])
def get_state():
    """Returns the current real-time state of the stadium (Mocking Firebase Sync)."""
    return jsonify(firebase_mock_state)

@app.route('/api/incentive', methods=['POST'])
def trigger_incentive():
    """Triggered by the Sensing simulator to dispatch vouchers."""
    data = request.json
    target_gate = data.get('target_gate', 'gate_b')
    
    # Update state: An active voucher campaign is launched
    firebase_mock_state['gates'][target_gate]['active_vouchers'] += 1
    logging.info(f"Voucher dispatched for {target_gate}")
    
    return jsonify({"status": "success", "message": "Incentives dispatched."}), 200

@app.route('/api/queue', methods=['POST'])
def virtual_queue():
    """Virtual Queue API: Issues timed QR-code windows."""
    user_id = request.json.get("user_id", "anonymous")
    
    # Calculate a queue time (e.g., 5 mins from now)
    pickup_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
    
    receipt = {
        "queue_id": str(uuid.uuid4()),
        "user_id": user_id,
        "pickup_time": pickup_time.strftime("%H:%M:%S"),
        "qr_payload": f"KINETIC-REQ-{uuid.uuid4().hex[:8]}"
    }
    
    firebase_mock_state['queues'].append(receipt)
    logging.info(f"Queue slot assigned: {receipt['queue_id']} at {receipt['pickup_time']}")
    
    return jsonify(receipt), 201

if __name__ == '__main__':
    # Binds to 8080. If deployed to Cloud Run, this handles the default exposed port.
    app.run(host='0.0.0.0', port=8080)
