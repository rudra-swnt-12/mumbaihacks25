import os
from twilio.rest import Client
from app.core.config import settings


class TwilioService:
    def __init__(self):
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = Client(
                settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
            )
            self.from_number = settings.TWILIO_PHONE_NUMBER
            self.enabled = True
        else:
            print("Twilio Keys missing. Calls will be simulated logs only.")
            self.enabled = False

    def make_call(self, to_number: str):
        """
        Triggers a call with a TwiML message.
        """
        if not self.enabled:
            print(f"Calling {to_number}...")
            return "simulated_sid"

        try:
            ngrok_url = os.getenv("NGROK_URL", "")
            clean_url = (
                ngrok_url.replace("https://", "").replace("http://", "").strip("/")
            )

            if not clean_url:
                print("Error: NGROK_URL is missing in .env")
                return None

            wss_url = f"wss://{clean_url}/ws/phone_stream"
            print(f"Twilio connecting to: {wss_url}")

            print(f"Dialing {to_number}...")

            twiml_content = f"""
            <Response>
                <Connect>
                    <Stream url="{wss_url}" />
                </Connect>
            </Response>
            """

            call = self.client.calls.create(
                twiml=twiml_content, to=to_number, from_=self.from_number
            )
            return call.sid

        except Exception as e:
            print(f"Twilio Call Error: {e}")
            return None

    def send_sms(self, to_number: str, message: str):
        """Sends an SMS alert or OTP."""
        if not self.enabled:
            print(f"SMS to {to_number}: {message}")
            return "simulated_msg_sid"

        try:
            print(f"Sending SMS to {to_number}...")
            msg = self.client.messages.create(
                body=message, from_=self.from_number, to=to_number
            )
            return msg.sid
        except Exception as e:
            print(f"Twilio SMS Error: {e}")
            return None
