from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import base64
import asyncio
import random
from datetime import datetime

from app.services.twilio_service import TwilioService
from app.core.config import settings
from app.services.weather_service import WeatherService
from app.services.deepgram_service import DeepgramService
from app.services.groq_service import GroqService
from app.services.tts_service import TTSService
from app.services.audio_analysis import AudioAnalyzer

from app.agents.checkin_agent import CheckinAgent
from app.services.asr_correction import ASRCorrectionService
from app.agents.onboarding_agent import OnboardingAgent
from app.agents.medication_agent import MedicationAgent
from app.agents.soap_agent import SOAPAgent
from app.core.database import SessionLocal, Patient, Consultation, Doctor

router = APIRouter()


@router.websocket("/ws/phone_stream")
async def phone_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Phone Call Connected")

    twilio_service = TwilioService()
    onboarding_agent = OnboardingAgent()
    med_agent = MedicationAgent()
    checkin_agent = CheckinAgent()
    soap_agent = SOAPAgent()

    asr_service = ASRCorrectionService()
    weather_service = WeatherService()
    stt_service = DeepgramService()
    groq_service = GroqService()
    tts_service = TTSService()
    audio_analyzer = AudioAnalyzer()

    call_state = {"is_registered": False, "patient_id": None}
    chat_history = []
    alert_sent = False

    stream_sid = None
    audio_buffer = bytearray()
    BUFFER_LIMIT = 40000

    try:
        weather = await weather_service.get_current_weather()
    except:
        weather = {"temp": "Unknown"}

    async def process_audio_buffer(buffer_data):
        nonlocal alert_sent

        if len(buffer_data) < 500:
            return

        try:
            is_slurred = audio_analyzer.detect_slur(buffer_data)
            if is_slurred:
                print("BIOMARKER ALERT: SLUR DETECTED")
                if not alert_sent and settings.NEIGHBOR_PHONE_NUMBER:
                    print("L2 ESCALATION: Notifying Neighbor...")
                    try:
                        twilio_service.send_sms(
                            settings.NEIGHBOR_PHONE_NUMBER,
                            f"URGENT: Arogya Saathi detected slurred speech. Please check on the patient.",
                        )
                        alert_sent = True
                    except:
                        pass
        except:
            pass

        candidates = await stt_service.transcribe_audio(
            bytes(buffer_data), is_phone=True
        )

        if candidates:
            raw_text = candidates[0]["text"]
            if not raw_text or len(raw_text.strip()) < 2:
                return

            primary_transcript = raw_text

            print(f"User: {primary_transcript}")
            chat_history.append(f"User: {primary_transcript}")

            response_text = ""

            if not call_state["is_registered"]:
                if len(primary_transcript) < 3:
                    return

                schema_keys = list(onboarding_agent.get_profile().keys())
                extracted_data = await groq_service.extract_profile_data(
                    primary_transcript, schema_keys
                )
                print(f"Extracted: {extracted_data}")

                prev_profile = onboarding_agent.get_profile().copy()
                onboarding_agent.update_state(extracted_data)
                curr_profile = onboarding_agent.get_profile()

                newly_filled = []
                for k, v in curr_profile.items():
                    if prev_profile[k] is None and v is not None:
                        newly_filled.append(k)

                print(f"Newly Filled: {newly_filled}")

                if onboarding_agent.is_complete:
                    if not call_state["is_registered"]:
                        call_state["is_registered"] = True
                        print("Saving Patient to Database...")

                        db = SessionLocal()
                        try:
                            profile = onboarding_agent.get_profile()
                            new_patient = Patient(
                                phone_number=f"+91{random.randint(7000000000, 9999999999)}",
                                full_name=profile.get("name"),
                                age=int(profile.get("age"))
                                if profile.get("age")
                                else 0,
                                location=profile.get("location"),
                                condition=profile.get("condition"),
                                is_onboarded=True,
                                created_at=datetime.now().isoformat(),
                            )
                            db.add(new_patient)
                            db.commit()
                            call_state["patient_id"] = new_patient.id
                            print(f"Saved DB ID: {new_patient.id}")
                        except Exception as e:
                            print(f"DB Error: {e}")
                        finally:
                            db.close()

                        response_text = f"Shukriya {profile.get('name')}. Aapka health card ban gaya hai. Ab bataiye, aaj kya takleef hai?"
                else:
                    instruction = onboarding_agent.generate_next_instruction()

                    acknowledgement_hint = ""
                    if newly_filled:
                        acknowledgement_hint = f"User just provided their {newly_filled[0]}. Acknowledge it warmly."
                    else:
                        acknowledgement_hint = (
                            "User answer was unclear. Politely ask again."
                        )

                    onboarding_context = f"""
                    SYSTEM MODE: EMPATHETIC DOCTOR ASSISTANT.
                    
                    CURRENT STATUS:
                    - Recorded so far: {curr_profile}
                    - MISSING DATA (Next Goal): {instruction}
                    
                    USER JUST SAID: "{primary_transcript}"
                    
                    INSTRUCTION:
                    1. {acknowledgement_hint}
                    2. Then, gently transition to the NEXT GOAL: "{instruction}".
                    
                    RULES:
                    - Speak ONLY in Hindi/Hinglish.
                    - Be warm and patient.
                    - Do NOT invent names (like Shanti). Address user by name ONLY if known.
                    """

                    _, response_text = await groq_service.generate_response(
                        primary_transcript, context=onboarding_context
                    )

            else:
                med_msg, med_context = med_agent.process(primary_transcript)
                current_med_state = med_agent.get_status()
                guidance = checkin_agent.determine_next_move(
                    primary_transcript, current_med_state
                )
                clinical_risk = checkin_agent.get_risk_score()

                triage_context = f"""
                Patient on Phone. 
                CLINICAL STATUS: {clinical_risk}
                OBJECTIVE: {guidance}
                {f"MEDICATION STATUS: {med_context}" if med_context else ""}
                """
                _, response_text = await groq_service.generate_response(
                    primary_transcript, context=triage_context
                )

            print(f"Agent: {response_text}")

            # TTS Pipeline
            is_first_chunk = True
            async for audio_chunk in tts_service.generate_audio(
                response_text, is_phone=True
            ):
                if is_first_chunk:
                    is_first_chunk = False
                    if audio_chunk.startswith(b"RIFF"):
                        try:
                            header_end = audio_chunk.find(b"data")
                            if header_end != -1:
                                audio_chunk = audio_chunk[header_end + 8 :]
                        except:
                            pass

                if len(audio_chunk) > 0:
                    b64_audio = base64.b64encode(audio_chunk).decode("utf-8")
                    await websocket.send_json(
                        {
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {"payload": b64_audio},
                        }
                    )

    try:
        while True:
            try:
                message_text = await asyncio.wait_for(
                    websocket.receive_text(), timeout=0.9
                )
                data = json.loads(message_text)

                if data["event"] == "start":
                    stream_sid = data["start"]["streamSid"]
                    print(f"Stream Started: {stream_sid}")

                    # Doctor Greeting
                    db = SessionLocal()
                    greeting_text = "Namaste! Main Arogya Saathi hoon."
                    try:
                        doctor = db.query(Doctor).first()
                        if doctor and doctor.custom_greeting:
                            greeting_text = doctor.custom_greeting.format(
                                name=doctor.full_name or "Doctor"
                            )
                    except Exception as e:
                        print(f"Greeting Error: {e}")
                    finally:
                        db.close()

                    if "?" not in greeting_text:
                        greeting_text += " Kripya apna naam batayein."

                    print(f"Init Greeting: {greeting_text}")

                    is_first_chunk = True
                    async for audio_chunk in tts_service.generate_audio(
                        greeting_text, is_phone=True
                    ):
                        if is_first_chunk:
                            is_first_chunk = False
                            if audio_chunk.startswith(b"RIFF"):
                                try:
                                    header_end = audio_chunk.find(b"data")
                                    if header_end != -1:
                                        audio_chunk = audio_chunk[header_end + 8 :]
                                except:
                                    pass
                        if len(audio_chunk) > 0:
                            b64_audio = base64.b64encode(audio_chunk).decode("utf-8")
                            await websocket.send_json(
                                {
                                    "event": "media",
                                    "streamSid": stream_sid,
                                    "media": {"payload": b64_audio},
                                }
                            )
                    continue

                if data["event"] == "media":
                    chunk = base64.b64decode(data["media"]["payload"])
                    audio_buffer.extend(chunk)
                    if len(audio_buffer) >= BUFFER_LIMIT:
                        await process_audio_buffer(audio_buffer)
                        audio_buffer = bytearray()

            except asyncio.TimeoutError:
                if len(audio_buffer) > 0:
                    await process_audio_buffer(audio_buffer)
                    audio_buffer = bytearray()

    except WebSocketDisconnect:
        print("Call Ended")
        if call_state["patient_id"] and len(chat_history) > 0:
            try:
                report_json = await soap_agent.generate_report(
                    chat_history, str(onboarding_agent.get_profile())
                )
                report_data = json.loads(report_json)
                db = SessionLocal()
                new_log = Consultation(
                    patient_id=call_state["patient_id"],
                    timestamp=datetime.now().isoformat(),
                    summary=report_data.get("summary", "Summary unavailable"),
                    risk_score=report_data.get("risk_score", 0),
                )
                db.add(new_log)
                db.commit()
                print("SOAP Note Saved!")
                db.close()
            except Exception as e:
                print(f"SOAP Error: {e}")
    except Exception as e:
        print(f"Call Error: {e}")
