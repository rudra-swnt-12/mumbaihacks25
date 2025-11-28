from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.deepgram_service import DeepgramService
from app.services.groq_service import GroqService
from app.services.tts_service import TTSService
from app.services.twilio_service import TwilioService
from app.services.audio_analysis import AudioAnalyzer
from app.agents.triage_agent import TriageAgent
from app.agents.nudge_agent import NudgeAgent
from app.agents.medication_agent import MedicationAgent
from app.agents.checkin_agent import CheckinAgent
from app.services.weather_service import WeatherService
from app.core.config import settings
import asyncio

router = APIRouter()


@router.websocket("/ws/listen")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Frontend Connected to WebSocket")

    stt_service = DeepgramService()
    groq_service = GroqService()
    tts_service = TTSService()
    twilio_service = TwilioService()
    audio_analyzer = AudioAnalyzer()
    weather_service = WeatherService()
    triage_agent = TriageAgent()
    nudge_agent = NudgeAgent()
    med_agent = MedicationAgent()
    checkin_agent = CheckinAgent()

    current_patient_context = "Patient: Shanti, Age: 60, Condition: Type 2 Diabetes"
    neighbor_phone = settings.NEIGHBOR_PHONE_NUMBER
    chat_history = []

    try:
        weather = await weather_service.get_current_weather()
        print(f"Local Weather: {weather}")
    except:
        weather = {"temp": "Unknown"}

    try:
        while True:
            audio_data = await websocket.receive_bytes()

            is_slurred = audio_analyzer.detect_slur(audio_data)
            slur_warning = ""

            if is_slurred:
                print("ALERT: Slurred speech detected")
                slur_warning = "[WARNING: Patient speech sounds SLURRED/DRUNK. Possible Hypoglycemia or Stroke.]"
                await websocket.send_json(
                    {
                        "type": "log",
                        "message": "ALERT: Slurred Speech Pattern Detected",
                    }
                )

            transcript = await stt_service.transcribe_audio(audio_data)

            if transcript and len(transcript.strip()) > 0:
                print(f"User: {transcript}")

                await websocket.send_json(
                    {"type": "log", "message": f"User: {transcript}"}
                )

                reflex_audio, keyword, is_hit = triage_agent.check_reflex(transcript)

                if is_hit:
                    await websocket.send_bytes(reflex_audio)
                    await websocket.send_json(
                        {
                            "type": "log",
                            "message": f"REFLEX TRIGGERED: '{keyword}' (Skipped LLM)",
                        }
                    )
                    continue

                med_status, med_context = med_agent.process(transcript)
                if med_status:
                    await websocket.send_json(
                        {"type": "log", "message": f"MEDICATION UPDATE: {med_status}"}
                    )

                urgency = triage_agent.analyze_urgency(transcript)

                if is_slurred:
                    urgency["priority"] = "CRITICAL"
                    urgency["msg"] = "Patient has Slurred Speech + Symptoms."

                guidance = ""

                if urgency["priority"] == "CRITICAL":
                    guidance = f"EMERGENCY PROTOCOL: {urgency['msg']}. Keep it short."
                else:
                    med_status = med_agent.get_status()
                    guidance = checkin_agent.determine_next_move(transcript, med_status)

                    await websocket.send_json(
                        {"type": "log", "message": f"AGENDA: {guidance}"}
                    )

                    if neighbor_phone:
                        await websocket.send_json(
                            {
                                "type": "log",
                                "message": f"Dialing Neighbor ({neighbor_phone})...",
                            }
                        )
                        call_sid = twilio_service.make_call(neighbor_phone)
                        if call_sid:
                            await websocket.send_json(
                                {
                                    "type": "log",
                                    "message": f"Call Initiated (SID: {call_sid})",
                                }
                            )
                    else:
                        await websocket.send_json(
                            {"type": "log", "message": "No Neighbor Phone Configured"}
                        )

                selected_action = nudge_agent.select_action()
                await websocket.send_json(
                    {
                        "type": "log",
                        "message": f"Strategy: {selected_action['name']} (Conf: {selected_action['confidence']:.2f})",
                    }
                )

                await websocket.send_json(
                    {"type": "log", "message": "Aarogya Thinking..."}
                )
                med_prompt = f"Medication Status: {med_context}" if med_context else ""

                dynamic_context = f"""
                {current_patient_context}.
                CURRENT OBJECTIVE: {guidance}
                Medical Protocol: {urgency["msg"]}.
                Tone: {selected_action["strategy"]["prompt"]}
                {med_prompt}
                """

                reasoning, response_text = await groq_service.generate_response(
                    transcript, context=dynamic_context
                )

                await websocket.send_json(
                    {"type": "log", "message": f"MEDPROMPT: {reasoning}"}
                )

                await websocket.send_json(
                    {"type": "log", "message": f"Response: {response_text}"}
                )

                try:
                    async for audio_chunk in tts_service.generate_audio(response_text):
                        await websocket.send_bytes(audio_chunk)

                    nudge_agent.update(selected_action["index"], reward=1)

                except Exception as e:
                    print(f"TTS Error: {e}")
                    await websocket.send_json(
                        {"type": "error", "message": "TTS Failed"}
                    )

    except WebSocketDisconnect:
        print("Client Disconnected")
    except Exception as e:
        print(f"Critical Error: {e}")
        await websocket.close()
