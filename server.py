from flask import Flask, jsonify, request
import hashlib
import json
import logging
import random

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# In-memory mock hardware state
propulsion_state = {
    "baseline_gravity": 9.80000,
    "current_resonance": 9.80100,
    "drift_percentage": 0.0102,
    "mode": "Active-Adjustment",
    "altitude": 12000.0,
    "security_lockdown": False
}

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    """Returns the current real-time state of the propulsion field."""
    # Simulate dynamic flux
    if not propulsion_state["security_lockdown"]:
        propulsion_state["current_resonance"] += random.uniform(-0.005, 0.005)
        drift = abs(propulsion_state["current_resonance"] - propulsion_state["baseline_gravity"])
        propulsion_state["drift_percentage"] = (drift / propulsion_state["baseline_gravity"]) * 100
        
        if propulsion_state["drift_percentage"] < 0.001:
            propulsion_state["mode"] = "Low-Latency/High-Efficiency"
        else:
            propulsion_state["mode"] = "Active-Adjustment"
            
    return jsonify(propulsion_state)

@app.route('/api/security/auto-level', methods=['POST'])
def trigger_auto_level():
    """Initiates Auto-Leveling safe mode and encrypts logs when anomalous telemetry is encountered."""
    payload = request.json
    
    # Encrypt the bad command/log
    raw_data = json.dumps(payload).encode('utf-8')
    encrypted_log = hashlib.sha256(raw_data).hexdigest()
    
    # Lock system
    propulsion_state["security_lockdown"] = True
    propulsion_state["mode"] = "Auto-Leveling Safe Mode"
    propulsion_state["current_resonance"] = 9.80000 
    propulsion_state["drift_percentage"] = 0.0000
    
    logging.critical(f"SPOOF DETECTED. Auto-level engaged. Log Encrypted: {encrypted_log}")
    
    return jsonify({"status": "locked", "encrypted_audit": encrypted_log}), 200

@app.route('/api/security/reset', methods=['POST'])
def reset_system():
    """Restores nominal operation from Auto-Level mode"""
    propulsion_state["security_lockdown"] = False
    propulsion_state["mode"] = "Low-Latency/High-Efficiency"
    return jsonify({"status": "nominal"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
