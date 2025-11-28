import httpx
import struct
from app.core.config import settings
from app.core.exceptions import STTError


class DeepgramService:
    def __init__(self):
        self.api_key = settings.DEEPGRAM_API_KEY
        self.url = "https://api.deepgram.com/v1/listen"

    def create_wav_header(self, data: bytes) -> bytes:
        total_size = 36 + len(data)
        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF",
            total_size,
            b"WAVE",
            b"fmt ",
            16,
            7,
            1,
            8000,
            8000,
            1,
            8,
            b"data",
            len(data),
        )
        return header + data

    async def transcribe_audio(self, audio_data: bytes, is_phone: bool = False):
        if not audio_data:
            return []

        keywords = [
            "chakkar:2",
            "pasina:2",
            "dard:2",
            "bukhaar:2",
            "saans:2",
            "ghabrahat:2",
            "ulti:2",
            "kamzori:2",
            "khansi:2",
            "sardi:2",
            "dast:2",
            "behoshi:2",
            "seene:2",
            "chaati:2",
            "haath:2",
            "pair:2",
            "pet:2",
            "sar:2",
            "gala:2",
            "sugar:2",
            "bp:2",
            "pressure:2",
            "goli:2",
            "dawa:2",
            "insulin:2",
            "attack:2",
            "shanti:2",
            "namaste:2",
            "theek:2",
            "haan:2",
            "nahi:2",
            "hello:2",
        ]

        params = {
            "model": "nova-2",
            "smart_format": "true",
            "language": "hi",
            "sample_rate": 8000,
            "keywords": keywords,
            "encoding": "mulaw",
            # "alternatives": 3,  Not supported by Nova-2 Model. N-Best Alternatives Feature is disabled for Nova-2 Model
        }
        if is_phone:
            audio_payload = self.create_wav_header(audio_data)
            headers = {
                "Authorization": f"Token {self.api_key}",
                "Content-Type": "audio/wav",
            }
            params["encoding"] = "mulaw"
            params["sample_rate"] = 8000
        else:
            audio_payload = audio_data
            headers = {
                "Authorization": f"Token {self.api_key}",
                "Content-Type": "audio/*",
            }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.url,
                    headers=headers,
                    params=params,
                    content=audio_payload,
                    timeout=10.0,
                )

                if response.status_code != 200:
                    raise STTError(
                        f"Deepgram API Error: {response.status_code}",
                        details={"body": response.text},
                    )

                data = response.json()

                try:
                    alt = data["results"]["channels"][0]["alternatives"][0]

                    if alt["transcript"].strip():
                        return [
                            {"text": alt["transcript"], "confidence": alt["confidence"]}
                        ]
                    return []

                except (KeyError, IndexError):
                    return []

        except httpx.RequestError as e:
            print(f"STT Connection Failed: {str(e)}")
            return []
        except Exception as e:
            print(f"Transcription Parsing Failed: {str(e)}")
            return []
