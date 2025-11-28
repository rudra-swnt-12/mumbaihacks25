from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db, Patient, Consultation
from app.services.twilio_service import TwilioService
from app.services.groq_service import GroqService
from pydantic import BaseModel

router = APIRouter(prefix="/patient", tags=["Patient Actions"])
twilio_service = TwilioService()
groq_service = GroqService()


class CallRequest(BaseModel):
    phone_number: str


@router.post("/trigger-call")
async def trigger_call_me(request: CallRequest, db: Session = Depends(get_db)):
    """
    Handles the 'Call Me' button press on the Patient Home Screen.
    """
    # Verify User
    user = db.query(Patient).filter_by(phone_number=request.phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Trigger Call
    print(f"User {user.full_name} requested a call.")
    sid = twilio_service.make_call(request.phone_number)

    return {"status": "calling", "sid": sid}


@router.get("/{phone_number}/memory-greeting")
async def get_memory_greeting(phone_number: str, db: Session = Depends(get_db)):
    """
    Generates the 'Memory' bubble at the top of the chat.
    """
    user = db.query(Patient).filter_by(phone_number=phone_number).first()
    if not user:
        return {"message": "Hello! How are you feeling today?"}

    # Get last consultation
    last_log = (
        db.query(Consultation)
        .filter_by(patient_id=user.id)
        .order_by(Consultation.id.desc())
        .first()
    )

    if not last_log:
        return {"message": f"Namaste {user.full_name}. How can I help you today?"}

    # Generate Contextual Greeting via Groq
    prompt = f"""
    Generate a warm, 1-sentence greeting for a patient based on their last visit.
    
    LAST VISIT SUMMARY: "{last_log.summary}"
    
    TASK: Ask about the specific issue mentioned last time.
    EXAMPLE: "Yesterday you mentioned dizziness. How is that feeling now?"
    OUTPUT: Just the sentence in Hinglish.
    """

    try:
        completion = await groq_service.client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="llama-3.1-8b-instant",
            max_tokens=60,
        )
        return {"message": completion.choices[0].message.content}
    except:
        return {"message": "Welcome back. How are you feeling?"}


@router.get("/{phone_number}/export-report")
async def export_data(phone_number: str, db: Session = Depends(get_db)):
    """
    Aggregates all data for the 'Download Report' button.
    """
    user = db.query(Patient).filter_by(phone_number=phone_number).first()
    if not user:
        raise HTTPException(status_code=404)

    history = db.query(Consultation).filter_by(patient_id=user.id).all()

    return {
        "patient_profile": {
            "name": user.full_name,
            "age": user.age,
            "conditions": user.condition,
        },
        "medical_history": [
            {"date": log.timestamp, "risk": log.risk_score, "notes": log.summary}
            for log in history
        ],
    }
