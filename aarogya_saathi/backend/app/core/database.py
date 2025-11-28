import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Boolean,
    JSON,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aarogya.db")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    doctor = relationship("Doctor", back_populates="patients")

    full_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    location = Column(String, nullable=True)
    condition = Column(String, nullable=True)
    existing_conditions = Column(Text, nullable=True)
    allergies = Column(String, nullable=True)

    last_glucose = Column(String, default="Unknown")
    medication_adherence = Column(Integer, default=0)

    role = Column(String, default="patient")
    is_onboarded = Column(Boolean, default=False)
    created_at = Column(String, nullable=True)

    consultations = relationship("Consultation", back_populates="patient")
    posts = relationship("CommunityPost", back_populates="patient")


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(String)
    summary = Column(Text)
    risk_score = Column(Integer)

    patient = relationship("Patient", back_populates="consultations")


class BanditState(Base):
    __tablename__ = "bandit_state"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, unique=True)
    alpha = Column(JSON)
    beta = Column(JSON)


class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("patients.id"))
    author_name = Column(String)

    content = Column(Text)
    category = Column(String)
    timestamp = Column(String)

    likes = Column(Integer, default=0)
    is_flagged = Column(Boolean, default=False)
    ai_response = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="posts")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)

    full_name = Column(String, nullable=True)
    custom_greeting = Column(
        String, default="Namaste! Main Doctor {name} ka AI assistant hoon."
    )
    specialization = Column(String, default="General Physician")
    hospital_name = Column(String, nullable=True)
    license_id = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)

    is_verified = Column(Boolean, default=False)
    created_at = Column(String, nullable=True)

    patients = relationship("Patient", back_populates="doctor")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
