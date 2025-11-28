from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.twilio_service import TwilioService
from app.core.config import settings
from pydantic import BaseModel
from passlib.context import CryptContext
from app.core.database import get_db, Patient, Doctor
from app.core.schemas import LoginRequest, VerifyRequest, DoctorLoginRequest
import random

router = APIRouter()
twilio_service = TwilioService()

otp_storage = {}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class GreetingUpdate(BaseModel):
    phone_number: str
    new_greeting: str


class LoginRequest(BaseModel):
    phone_number: str
    role: str


class VerifyRequest(BaseModel):
    phone_number: str
    otp: str
    role: str


@router.post("/auth/send-otp")
async def send_otp(request: LoginRequest, db: Session = Depends(get_db)):
    """
    1. Checks/Creates user in DB based on ROLE.
    2. Generates OTP.
    3. Sends SMS.
    """
    phone = request.phone_number

    if request.role == "doctor":
        user = db.query(Doctor).filter(Doctor.phone_number == phone).first()
        if not user:
            user = Doctor(
                phone_number=phone, full_name="New Doctor", specialization="General"
            )
            db.add(user)
            db.commit()
    else:
        user = db.query(Patient).filter(Patient.phone_number == phone).first()
        if not user:
            user = Patient(
                phone_number=phone,
                full_name="New Patient",
                age=0,
                condition="Unknown",
                is_onboarded=False,
            )
            db.add(user)
            db.commit()

    otp = str(random.randint(1000, 9999))
    otp_storage[phone] = otp

    print(f"GENERATED OTP for {phone} ({request.role}): {otp}")

    target_phone = (
        settings.NEIGHBOR_PHONE_NUMBER if settings.NEIGHBOR_PHONE_NUMBER else phone
    )

    message = f"Arogya Code: {otp}"
    sid = twilio_service.send_sms(target_phone, message)

    if sid:
        return {"status": "success", "message": "OTP Sent", "debug_otp": otp}
    else:
        return {
            "status": "success",
            "message": "OTP Generated (Simulated)",
            "debug_otp": otp,
        }


@router.post("/auth/verify-otp")
async def verify_otp(request: VerifyRequest, db: Session = Depends(get_db)):
    """
    Verifies OTP and returns the Real Database Record.
    """
    stored_otp = otp_storage.get(request.phone_number)

    if stored_otp and stored_otp == request.otp:
        del otp_storage[request.phone_number]

        if request.role == "doctor":
            doctor = (
                db.query(Doctor)
                .filter(Doctor.phone_number == request.phone_number)
                .first()
            )
            if not doctor:
                raise HTTPException(status_code=404, detail="Doctor not found")

            return {
                "status": "success",
                "role": "doctor",
                "data": {
                    "id": doctor.id,
                    "name": doctor.full_name,
                    "specialization": doctor.specialization,
                    "custom_greeting": doctor.custom_greeting,
                    "is_verified": doctor.is_verified,
                },
            }
        else:
            patient = (
                db.query(Patient)
                .filter(Patient.phone_number == request.phone_number)
                .first()
            )
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")

            return {
                "status": "success",
                "role": "patient",
                "patient_data": {
                    "id": patient.id,
                    "name": patient.full_name or "Unknown",
                    "age": patient.age,
                    "condition": patient.condition or "Unknown",
                    "last_glucose": patient.last_glucose,
                    "medication_adherence": f"{patient.medication_adherence}%",
                    "location": patient.location,
                    "alerts": ["Routine Check-up Due"]
                    if patient.medication_adherence > 50
                    else ["Risk: High Adherence Issue"],
                },
            }

    raise HTTPException(status_code=400, detail="Invalid OTP")


@router.put("/doctor/update-greeting")
async def update_greeting(request: GreetingUpdate, db: Session = Depends(get_db)):
    doctor = (
        db.query(Doctor).filter(Doctor.phone_number == request.phone_number).first()
    )
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.custom_greeting = request.new_greeting
    db.commit()

    return {
        "status": "success",
        "message": "Greeting updated!",
        "greeting": doctor.custom_greeting,
    }


@router.post("/auth/doctor-login")
async def doctor_login(request: DoctorLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates a Doctor using their license_id and password/hashed_password.
    """
    doctor = db.query(Doctor).filter(Doctor.license_id == request.doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Invalid ID or Password")
    
    if settings.DEMO_MASTER_PASSWORD and request.password == settings.DEMO_MASTER_PASSWORD:
        pass 
    elif doctor.hashed_password is None:
        raise HTTPException(status_code=401, detail="Account not configured. Use demo password.")
    elif not pwd_context.verify(request.password, doctor.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid ID or Password")

    return {
        "status": "success",
        "role": "doctor",
        "data": {
            "id": doctor.id,
            "name": doctor.full_name,
            "specialization": doctor.specialization,
            "custom_greeting": doctor.custom_greeting,
            "is_verified": doctor.is_verified
        }
    }


@router.put("/patient/update-profile")
async def update_patient_profile(request: ProfileUpdate, db: Session = Depends(get_db)):
    """
    Allows the patient to update their profile details from the web/app form.
    """
    patient = db.query(Patient).filter(Patient.phone_number == request.phone_number).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient.full_name = request.full_name
    patient.age = request.age
    patient.gender = request.gender
    
    patient.is_onboarded = True
    db.commit()

    return {"status": "success", "message": "Profile updated successfully."}