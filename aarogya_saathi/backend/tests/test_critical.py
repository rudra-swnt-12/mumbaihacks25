import asyncio
import websockets
import json
import os

# CONFIGURATION
URI = "ws://localhost:8000/ws/listen"

# Path Setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_AUDIO_FILE = os.path.join(
    SCRIPT_DIR, "..", "critical_input.mp3"
)  # <--- Specific file
OUTPUT_AUDIO_FILE = os.path.join(SCRIPT_DIR, "critical_response.mp3")


async def run_critical_test():
    print(f"🚑 STARTING CRITICAL ESCALATION TEST...")
    print(f"🔌 Connecting to {URI}...")

    # Bypass CORS
    async with websockets.connect(
        URI, additional_headers={"Origin": "http://localhost:3000"}
    ) as websocket:
        print("✅ Connected!")

        # 1. Check File
        if not os.path.exists(INPUT_AUDIO_FILE):
            print(
                f"❌ Error: Please record 'critical_input.mp3' with words 'Chest Pain' and put it in the backend folder."
            )
            return

        # 2. Send Audio
        with open(INPUT_AUDIO_FILE, "rb") as f:
            audio_data = f.read()
            await websocket.send(audio_data)
        print("outbox 📤 Audio sent. Listening for Escalation logs...")

        # 3. Listen for Twilio Logs
        with open(OUTPUT_AUDIO_FILE, "wb") as f_out:
            while True:
                try:
                    message = await websocket.recv()

                    if isinstance(message, str):
                        data = json.loads(message)
                        msg_text = data.get("message", "")

                        # --- SPECIAL LOGGING FOR TWILIO ---
                        if "CRITICAL" in msg_text:
                            print(f"\n🔴 [ALERT]: {msg_text}")
                        elif "Dialing" in msg_text:
                            print(f"📞 [TWILIO]: {msg_text}")
                        elif "Call Initiated" in msg_text:
                            print(f"✅ [SUCCESS]: {msg_text}")
                            print("🎉 YOUR PHONE SHOULD BE RINGING NOW!\n")
                        elif "type" in data and data["type"] == "log":
                            print(f"   log: {msg_text}")
                        elif "type" in data and data["type"] == "error":
                            print(f"❌ ERROR: {msg_text}")
                            break

                    elif isinstance(message, bytes):
                        f_out.write(message)

                except websockets.exceptions.ConnectionClosed:
                    print("🔌 Connection closed.")
                    break
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                    break


if __name__ == "__main__":
    asyncio.run(run_critical_test())
