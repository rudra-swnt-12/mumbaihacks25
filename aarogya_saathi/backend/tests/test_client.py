import asyncio
import websockets
import json
import os

# 1. CONFIGURATION
URI = "ws://localhost:8000/ws/listen"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# You need a sample audio file of someone speaking Hindi/English
# If you don't have one, record a quick "Hello" on your phone and save it here.
INPUT_AUDIO_FILE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "test_input.mp3"))
OUTPUT_AUDIO_FILE = os.path.join(SCRIPT_DIR, "response_output.mp3")


async def run_test():
    print(f"🔌 Connecting to {URI}...")
    print(f"🔍 SEARCHING FOR AUDIO AT: {INPUT_AUDIO_FILE}")

    if not os.path.exists(INPUT_AUDIO_FILE):
        print(f"❌ ERROR: File does not exist at that path.")
        print(
            f"👉 Tip: Move your mp3 file to the 'backend' folder or rename it to 'test_input.mp3'"
        )
        return

    async with websockets.connect(
        URI, additional_headers={"Origin": "http://localhost:3000"}
    ) as websocket:
        print("✅ Connected! Sending audio...")

        # 2. READ & SEND AUDIO

        with open(INPUT_AUDIO_FILE, "rb") as f:
            audio_data = f.read()
            await websocket.send(audio_data)

        print("📤 Audio sent. Waiting for response...")

        # 3. LISTEN FOR RESPONSES
        with open(OUTPUT_AUDIO_FILE, "wb") as f_out:
            while True:
                try:
                    message = await websocket.recv()

                    # CASE A: It's a JSON Log (Text)
                    if isinstance(message, str):
                        data = json.loads(message)
                        if data.get("type") == "log":
                            print(f"📝 LOG: {data['message']}")
                        elif data.get("type") == "error":
                            print(f"❌ ERROR: {data['message']}")
                            break

                    # CASE B: It's Audio Bytes (The Voice)
                    elif isinstance(message, bytes):
                        print(f"🔊 Received Audio Chunk ({len(message)} bytes)")
                        f_out.write(message)

                except websockets.exceptions.ConnectionClosed:
                    print("🔌 Connection closed by server.")
                    break
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                    break

        print(f"\n✅ Test Complete. Response audio saved to '{OUTPUT_AUDIO_FILE}'")


if __name__ == "__main__":
    # Install websockets client if you haven't: pip install websockets
    asyncio.run(run_test())
