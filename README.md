
## 403-Project---Smart-Classroom-Ventilation-Agent-System

## Setup
1. Open in GitHub Codespaces
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The system uses an external XMPP server (jabber.fr) for agent communication. The agent JIDs and password are defined at the top of `main.py`:
```python
SENSOR_JID      = "sensor_dcit403@jabber.fr"
COORDINATOR_JID = "coordinator_dcit403@jabber.fr"
VENTILATION_JID = "ventilation_dcit403@jabber.fr"
PASSWORD        = "dcit403pass"
```
No local XMPP server setup is required. Accounts are automatically registered on first run via `auto_register=True`.

## Run
```bash
python main.py
```

## Description

This system simulates a smart classroom ventilation system using the SPADE multi-agent framework. Three agents communicate over XMPP in real time:
- **SensorAgent** — simulates CO₂ and temperature readings and sends them to the Coordinator
- **CoordinatorAgent** — evaluates incoming data against thresholds and decides the appropriate action
- **VentilationAgent** — receives decisions and responds accordingly (open windows, activate cooling, or confirm normal conditions)

## Thresholds
- CO₂ limit: `1000 ppm`
- Temperature limit: `28°C`
