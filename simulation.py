import time
import random
import logging
import json
import hashlib

# Configure sub-5ms telemetry logging output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] ANTI-GRAV-CONTROLLER: %(message)s',
    datefmt='%H:%M:%S.%f'
)

class PropulsionSystem:
    def __init__(self):
        self.baseline_gravity = 9.80000  # m/s^2
        self.current_resonance = self.baseline_gravity
        self.altitude = 12000.0  # meters
        self.atmospheric_pressure = 19.3  # kPa at roughly 12km
        self.mode = "High-Efficiency"
        self.auto_leveling = False

    def sense_telemetry(self):
        # Simulate non-linear fluctuations in G-sensors
        fluctuation = random.uniform(-0.0005, 0.0005)
        
        # Random spoof/spike injection to trigger security protocol (1% chance)
        if random.random() < 0.01:
            fluctuation = random.uniform(5.0, 10.0)
            
        self.current_resonance += fluctuation
        self.altitude += random.uniform(-0.5, 0.5)
        
        return {
            "g_sensor": round(self.current_resonance, 5),
            "altimeter": round(self.altitude, 2),
            "pressure": round(self.atmospheric_pressure, 2)
        }

    def encrypt_logs(self, telemetry):
        # Simulate encrypting command logs during a spoof/breach
        raw_data = json.dumps(telemetry).encode('utf-8')
        encrypted = hashlib.sha256(raw_data).hexdigest()
        logging.warning(f"SECURITY PROTOCOL ACTIVE. Logs encrypted: {encrypted}")

    def stabilize(self, telemetry):
        g_drift = abs(telemetry["g_sensor"] - self.baseline_gravity)
        drift_percentage = (g_drift / self.baseline_gravity) * 100

        # Security Protocol: Out of bounds (> 5% drift indicates corruption/spoof)
        if drift_percentage > 5.0:
            self.auto_leveling = True
            self.mode = "Safe-Mode"
            logging.critical(f"TELEMETRY BOUNDARIES EXCEEDED (Drift: {drift_percentage:.4f}%). INITIATING AUTO-LEVELING.")
            self.encrypt_logs(telemetry)
            
            # Force resonance back to baseline drastically
            self.current_resonance = self.baseline_gravity
            time.sleep(0.5) # Represent locking parameters
            return

        elif self.auto_leveling and drift_percentage < 0.001:
            logging.info("Field stabilized. Disengaging Auto-Leveling.")
            self.auto_leveling = False

        # Stability Calibration: Calculate inverse modulation if drift > 0.001%
        if drift_percentage > 0.001 and not self.auto_leveling:
            self.mode = "Active-Adjustment"
            inverse_modulation = self.baseline_gravity - telemetry["g_sensor"]
            logging.info(f"Drift {drift_percentage:.4f}% detected. Executing micro-adjustment: {inverse_modulation:+.5f} m/s^2")
            
            # Apply counter-measure
            self.current_resonance += inverse_modulation

        # Efficiency Loop: Stable field
        elif drift_percentage <= 0.001 and not self.auto_leveling:
            if self.mode != "Low-Latency/High-Efficiency":
                self.mode = "Low-Latency/High-Efficiency"
                logging.info(f"System stable. Optimization routine shifted to: {self.mode}. Power-to-lift maximum.")
            else:
                logging.debug(f"Stable resonance. Mode: {self.mode}.")


def run_simulation():
    logging.info("Initializing Anti-Gravity Propulsion System Real-Time Stability Controller...")
    system = PropulsionSystem()
    
    # Simulating continuous sub-5ms cycles (sleep slightly longer for visual logging)
    try:
        while True:
            telemetry = system.sense_telemetry()
            system.stabilize(telemetry)
            time.sleep(0.1)  # Representing micro-cycle loops in terminal
    except KeyboardInterrupt:
        logging.info("Controller offline.")

if __name__ == "__main__":
    run_simulation()
