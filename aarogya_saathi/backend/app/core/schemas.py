from pydantic import BaseModel, Field
from typing import Optional, List


class PatientBase(BaseModel):
    phone_number: str = Field(..., description="Patient's primary contact number")
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    existing_conditions: Optional[str] = None
    allergies: Optional[str] = None
    doctor_id: Optional[int] = None


# Shanti (via Onboarding Agent)
class PatientCreate(PatientBase):
    pass


class ProfileUpdate(BaseModel):
    phone_number: str
    full_name: str
    age: int
    gender: str


# Consultation Logs for Doctor (via Portal)
class ConsultationResponse(BaseModel):
    id: int
    timestamp: str
    summary: str
    risk_score: Optional[int] = 0

    class Config:
        from_attributes = True


# Doctor (via Portal)
class PatientResponse(PatientBase):
    id: int
    is_onboarded: bool
    last_glucose: Optional[str] = "Unknown"
    adherence_score: Optional[int] = 0

    consultations: List[ConsultationResponse] = []

    class Config:
        from_attributes = True


class DoctorBase(BaseModel):
    phone_number: str
    full_name: Optional[str] = None
    specialization: Optional[str] = "General Physician"
    hospital_name: Optional[str] = None


class DoctorCreate(DoctorBase):
    license_id: str  # Mandatory


class DoctorResponse(DoctorBase):
    id: int
    is_verified: bool

    class Config:
        from_attributes = True


class DoctorLoginRequest(BaseModel):
    doctor_id: str
    password: str


class GreetingUpdate(BaseModel):
    phone_number: str
    new_greeting: str

# Input via Doctor (For Patient and Self)
class VitalsUpdate(BaseModel):
    phone_number: str
    glucose_reading: int
    clinical_status: str
    timestamp: Optional[str] = None


# Login AUTH
class LoginRequest(BaseModel):
    phone_number: str
    role: str


class VerifyRequest(BaseModel):
    phone_number: str
    otp: str
    role: str


# System Memory (via Bandit)
class BanditStateResponse(BaseModel):
    agent_name: str
    alpha: List[float]
    beta: List[float]

    class Config:
        from_attributes = True
