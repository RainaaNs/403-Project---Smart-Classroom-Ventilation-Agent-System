import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

SENSOR_JID      = "sensor_dcit403@jabber.fr"
COORDINATOR_JID = "coordinator_dcit403@jabber.fr"
VENTILATION_JID = "ventilation_dcit403@jabber.fr"
PASSWORD        = "dcit403pass"

CO2_THRESHOLD = 1000
TEMP_THRESHOLD = 28

# ---------------- SENSOR AGENT ----------------
class SensorAgent(Agent):
    class SendDataBehaviour(CyclicBehaviour):
        async def run(self):
            co2 = random.randint(400, 1500)
            temp = random.randint(20, 35)

            msg = Message(to=COORDINATOR_JID)
            msg.set_metadata("performative", "inform")
            msg.body = f"{co2},{temp}"

            print(f"[Sensor] CO2: {co2} ppm | Temp: {temp}°C")
            await self.send(msg)
            await asyncio.sleep(3)

    async def setup(self):
        print("[Sensor] Agent started")
        self.add_behaviour(self.SendDataBehaviour())


# ---------------- COORDINATOR AGENT ----------------
class CoordinatorAgent(Agent):
    class DecideBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                try:
                    co2, temp = map(int, msg.body.split(","))
                except ValueError:
                    print("[Coordinator] Bad message format, skipping.")
                    return

                if co2 > CO2_THRESHOLD:
                    action = "HIGH_CO2"
                elif temp > TEMP_THRESHOLD:
                    action = "HIGH_TEMP"
                else:
                    action = "NORMAL"

                print(f"[Coordinator] CO2: {co2}, Temp: {temp} → Decision: {action}")

                reply = Message(to=VENTILATION_JID)
                reply.set_metadata("performative", "request")
                reply.body = action
                await self.send(reply)

    async def setup(self):
        print("[Coordinator] Agent started")
        self.add_behaviour(self.DecideBehaviour())


# ---------------- VENTILATION AGENT ----------------
class VentilationAgent(Agent):
    class ActBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                action = msg.body
                if action == "HIGH_CO2":
                    print("[Ventilation] ⚠️  CO2 high — Suggesting: Open windows / Activating fans")
                elif action == "HIGH_TEMP":
                    print("[Ventilation] 🌡️  Temp high — Activating cooling system")
                elif action == "NORMAL":
                    print("[Ventilation] ✅  Air quality normal — No action needed")

    async def setup(self):
        print("[Ventilation] Agent started")
        self.add_behaviour(self.ActBehaviour())


# ---------------- MAIN ----------------
async def main():
    print("[System] Starting agents...\n")

    sensor      = SensorAgent(SENSOR_JID, PASSWORD)
    coordinator = CoordinatorAgent(COORDINATOR_JID, PASSWORD)
    ventilation = VentilationAgent(VENTILATION_JID, PASSWORD)

    await sensor.start(auto_register=True)
    await asyncio.sleep(1)
    await coordinator.start(auto_register=True)
    await asyncio.sleep(1)
    await ventilation.start(auto_register=True)
    await asyncio.sleep(1)

    print("\n[System] All agents running. Monitoring for 60 seconds...\n")

    try:
        await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("\n[System] Interrupted.")
    finally:
        print("\n[System] Stopping agents...")
        await sensor.stop()
        await coordinator.stop()
        await ventilation.stop()
        print("[System] All agents stopped.")


if __name__ == "__main__":
    asyncio.run(main())