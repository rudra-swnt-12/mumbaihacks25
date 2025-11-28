import sys
import os

# Get the absolute path of the 'backend' directory (one level up)
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_path)

import asyncio
import os
from app.services.groq_service import GroqService
from app.services.tts_service import TTSService
from app.services.deepgram_service import DeepgramService
from app.core.exceptions import AarogyaException


async def run_diagnostics():
    print("🏥 --- STARTING AAROGYA SYSTEM DIAGNOSTICS ---")

    # 1. Initialize Services
    try:
        groq = GroqService()
        tts = TTSService()
        deepgram = DeepgramService()
        print("✅ Services Initialized successfully.")
    except Exception as e:
        print(f"❌ Initialization Failed: {e}")
        return

    # 2. Test Groq (The Brain)
    print("\n🧠 Testing Groq (Llama-3)...")
    user_query = "Mujhe bohot chakkar aa rahe hain aur pasina aa raha hai."
    print(f"   User Input: '{user_query}'")

    generated_speech = ""

    try:
        reasoning, speech = await groq.generate_response(user_query)
        print(f"   ✅ [REASONING]: {reasoning}")
        print(f"   ✅ [RESPONSE]: {speech}")
        generated_speech = speech
    except AarogyaException as e:
        print(f"   ❌ Groq Failed: {e}")
        return

    # 3. Test ElevenLabs (The Mouth)
    print("\n🗣️  Testing ElevenLabs TTS (Streaming)...")
    audio_filename = "diagnostic_output.mp3"

    try:
        with open(audio_filename, "wb") as f:
            print("   Stream started...", end="", flush=True)
            chunk_count = 0
            async for chunk in tts.generate_audio(generated_speech):
                f.write(chunk)
                chunk_count += 1
                if chunk_count % 5 == 0:
                    print(".", end="", flush=True)
        print(f"\n   ✅ Audio saved to '{audio_filename}'")
    except AarogyaException as e:
        print(f"\n   ❌ TTS Failed: {e}")
        return

    # 4. Test Deepgram (The Ear)
    # We will try to transcribe the file we just created
    print("\n👂 Testing Deepgram STT...")

    try:
        # Read the file bytes we just saved
        with open(audio_filename, "rb") as f:
            audio_data = f.read()

        transcript = await deepgram.transcribe_audio(audio_data)
        print(f"   ✅ Transcribed back: '{transcript}'")
    except AarogyaException as e:
        print(f"   ❌ Deepgram Failed: {e}")
    except Exception as e:
        print(f"   ⚠️  Deepgram Warning: {e}")
        print("       (Note: Deepgram prerecorded might fail on tiny files < 1 sec)")

    print("\n✅ --- DIAGNOSTICS COMPLETE ---")


if __name__ == "__main__":
    # Run the async loop
    asyncio.run(run_diagnostics())
