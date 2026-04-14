# Walkthrough: Agent-Driven Interactions

The Kinetic Venue system treats each feature layer as a semi-autonomous "agent." Here's how these logic blocks interact to achieve the 100,000+ capacity crowd management goal.

## 1. The Sensor Agent (LiDAR Simulator)
- **Role**: Continuously maps the physical space.
- **Interaction**: In `simulation.py`, the `LiDARNode` class acts as this agent, running loops representing thousands of fans arriving every minute. It passes its findings upstream.

## 2. The Incentive Evaluator Agent
- **Role**: The brain of the operation.
- **Interaction**: The `MicroIncentiveEngine` receives the Sensor Agent's data. If it detects a variance (Gate A is filling up excessively), it makes a deterministic choice to execute a promotional campaign. It doesn't rely on human operators; it instantly pushes an event object (`ISSUE_VOUCHER`) toward the database.

## 3. The Synchronization Agent (Firebase)
- **Role**: Real-time state management.
- **Interaction**: When the Incentive Evaluator sends the payload, Firebase broadcasts this delta to all listening frontend clients (the stadium screens and user mobile devices).

## 4. The Virtual Queue API Agent
- **Role**: Dispersing long lines.
- **Interaction**: When fans route to Gate B (due to the incentive), the concession stands there get hit. The Virtual Queue Agent intercepts this demand. Instead of allowing humans to queue up, it issues unique QR payloads and schedules pickup windows.

## 5. HADM (Highly-Available Device Mesh) Conceptual Agent
- **Role**: Failsafe connectivity.
- **Interaction**: In a 100k capacity stadium, cell towers often fail. If the Synchronization Agent (Firebase) cannot reach the user's mobile device, the HADM agent relies on Bluetooth Low Energy to pass the incentive vouchers and queue QR codes peer-to-peer between devices until it reaches the user.
