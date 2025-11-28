import sys
import os

# --- PATH FIX ---
# Add the current directory to sys.path so Python can find the 'app' module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.twilio_service import TwilioService
from app.core.config import settings


def trigger_now():
    print("Initializing Manual Trigger...")

    # 1. Initialize Service
    service = TwilioService()

    # 2. Get Target Number from .env
    target_phone = settings.NEIGHBOR_PHONE_NUMBER

    if not target_phone:
        print("Error: NEIGHBOR_PHONE_NUMBER is missing in your .env file.")
        print("   -> Add it like this: NEIGHBOR_PHONE_NUMBER='+1234567890'")
        return

    # 3. Make the Call
    print(f"Dialing {target_phone} via Ngrok Tunnel...")
    sid = service.make_call(target_phone)

    # 4. Report Status
    if sid and sid != "simulated_sid":
        print(f"Call Initiated Successfully! SID: {sid}")
        print("ACTION REQUIRED: Pick up your phone and say 'Hello' to test the AI.")
    elif sid == "simulated_sid":
        print("Simulation Mode: Twilio keys are missing or invalid.")
    else:
        print("Call Failed. Check your Twilio credentials and Ngrok URL.")


if __name__ == "__main__":
    trigger_now()
