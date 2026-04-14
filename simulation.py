import time
import random
import json
import logging

# Configure terminal logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] KINETIC-ENGINE: %(message)s',
    datefmt='%H:%M:%S'
)

class LiDARNode:
    def __init__(self, gate_id):
        self.gate_id = gate_id
        self.density = random.uniform(10.0, 30.0)

    def sense(self):
        # Simulate active crowd buildup (random walk)
        self.density += random.uniform(-2.0, 5.0)
        self.density = max(0.0, min(100.0, self.density))
        return round(self.density, 2)

class MicroIncentiveEngine:
    def __init__(self, threshold=85.0):
        self.threshold = threshold
        self.active_campaign = False

    def evaluate(self, gate_id, density):
        if density >= self.threshold and not self.active_campaign:
            self.active_campaign = True
            logging.warning(f"CRITICAL BOTTLENECK PREDICTED at {gate_id} (Density: {density}%).")
            logging.info("Triggering Micro-Incentive Engine via Firebase...")
            self.dispatch_voucher(gate_id)
            return True
        elif density < 60.0 and self.active_campaign:
            self.active_campaign = False
            logging.info(f"Flow stabilized at {gate_id}. Concluding incentive campaign.")
        return False

    def dispatch_voucher(self, bottleneck_gate):
        target_gate = "Gate B" if bottleneck_gate == "Gate A" else "Gate A"
        payload = {
            "action": "ISSUE_VOUCHER",
            "incentive": "20% off Concessions",
            "condition": f"Route to {target_gate} within 5 mins"
        }
        logging.info(f"Firebase Sync -> {json.dumps(payload)}")

def run_simulation(capacity=100000, loops=20):
    logging.info(f"Starting KINETIC VENUE Simulation for {capacity} capacity stadium.")
    
    gate_a = LiDARNode("Gate A")
    gate_b = LiDARNode("Gate B")
    engine = MicroIncentiveEngine(threshold=80.0)
    
    for i in range(loops):
        time.sleep(1)
        den_a = gate_a.sense()
        den_b = gate_b.sense()
        
        logging.info(f"LiDAR Data -> Gate A: {den_a}%, Gate B: {den_b}%")
        
        triggered_a = engine.evaluate(gate_a.gate_id, den_a)
        
        # If incentive triggered, people start moving to gate B
        if triggered_a or engine.active_campaign:
            gate_a.density -= random.uniform(3.0, 8.0)
            gate_b.density += random.uniform(1.0, 4.0)

    logging.info("Simulation Complete. All systems nominal.")

if __name__ == "__main__":
    run_simulation()
