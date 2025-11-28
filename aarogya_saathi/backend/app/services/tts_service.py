import httpx
from app.core.config import settings
from app.core.exceptions import TTSError


class TTSService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.voice_id = settings.ELEVENLABS_VOICE_ID
        self.base_url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
        )

    async def generate_audio(self, text: str, is_phone: bool = False):
        """
        Generates audio stream.
        - is_phone=True: Requests 'ulaw_8000' (Required for Twilio Phone Calls)
        - is_phone=False: Requests 'mp3_44100_128' (Standard for Web Browser)
        """
        headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}

        output_format = "ulaw_8000" if is_phone else "mp3_44100_128"
        url_with_params = f"{self.base_url}?output_format={output_format}&optimize_streaming_latency=3"

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True,
            },
        }

        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST", url_with_params, json=data, headers=headers
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        raise TTSError(
                            f"ElevenLabs Error: {response.status_code}",
                            details={"error": error_text.decode()},
                        )

                    async for chunk in response.aiter_bytes():
                        if chunk:
                            yield chunk

        except httpx.RequestError as e:
            raise TTSError("Failed to connect to ElevenLabs", details={"error": str(e)})
