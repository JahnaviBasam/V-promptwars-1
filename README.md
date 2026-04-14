# KINETIC VENUE

## Overview
**Kinetic Venue** is an intelligent full-stack solution designed to orchestrate the physical fan experience at a 100,000-capacity sporting stadium. 

By leveraging predictive sensing models and a real-time Micro-Incentive Engine, Kinetic Venue actively prevents bottlenecks rather than just reacting to them.

## Core Features
1. **Predictive Crowd Map**: Ingests mock LiDAR data to map out arrival density at Gate A and Gate B.
2. **Micro-Incentive Engine**: When capacity near a gate exceeds a critical threshold, the engine automatically dispatches Firebase-backed "Early-Bird Vouchers" (e.g., *20% off concessions*) to redirect users proactively.
3. **Virtual Queue API**: Eliminates physical standing lines by providing scheduled QR-code time windows for concessions.
4. **HADM Peer-to-Peer**: Conceptual mesh-network protocol designed to facilitate group finding when stadium cellular networks become congested.

## Architectural Flow
```
[ Sensing Layer ] ---> [ Processing Engine ] ---> [ Action / Actionable Outputs ]
(LiDAR / Devices)      (Python / Next.js)       (Firebase / End User Devices)

1) SENSING: `simulation.py` runs as the ingestion node, producing continuous density data at Gate A & Gate B.
2) THRESHOLD DETECTION: When density > 80%, the Micro-Incentive logic intercepts the feed.
3) SYNCHRONIZATION: The backend pushes an alert payload directly to the Firebase Realtime Database.
4) DISPATCH: The UI (Dashboard) listens to Firebase state changes. It renders the bottleneck map and pushes notification banners to redirect fans.
5) RESOLUTION: Fans shift to the alternative gate. Density equilibrates. The Incentive campaign ends.
```

## Running the Prototype
*Since Node/Python dependencies vary, the prototype is separated into a standalone Dashboard and a sensing simulator.*

1. **Dashboard UI**: Open `index.html` in any modern browser. It automatically runs a standalone mock representation of the real-time Firebase synchronization.
2. **LiDAR Simulator**: Run `python simulation.py` in your terminal to see the raw text-based bottleneck prediction and incentive engine routing logic in action.

## Built With
- **Frontend**: HTML5, Vanilla Native CSS (Glassmorphism), JavaScript
- **Backend/Sim**: Python 3
- **Database (Conceptual/Mocked)**: Firebase Realtime Database