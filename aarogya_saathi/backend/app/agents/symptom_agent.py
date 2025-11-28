"""
SymptomAgent - Analyzes symptoms and provides doctor-like medical advice context.
"""


class SymptomAgent:
    def __init__(self):
        # Common symptoms and their medical advice context
        self.symptom_database = {
            # Fever related
            "fever": {
                "keywords": ["fever", "bukhar", "buxar", "temperature", "tez bukhar", "halka bukhar", "garmi"],
                "advice": "Patient reports fever. Advise: Rest, stay hydrated, take paracetamol if temperature exceeds 101°F. Monitor temperature. Seek immediate care if fever persists beyond 3 days or exceeds 103°F.",
                "questions": ["How many days have you had fever?", "What is your temperature if measured?", "Any other symptoms like body pain or headache?"]
            },
            # Cough related
            "cough": {
                "keywords": ["cough", "khansi", "khasi", "khaansi", "dry cough", "sukhi khansi", "balgam", "phlegm"],
                "advice": "Patient reports cough. Advise: Warm water with honey, steam inhalation, avoid cold drinks. If cough has blood or persists beyond 2 weeks, seek immediate medical attention.",
                "questions": ["Is it dry cough or with phlegm?", "How long have you had cough?", "Any difficulty breathing?"]
            },
            # Cold related
            "cold": {
                "keywords": ["cold", "sardi", "nazla", "zukam", "runny nose", "blocked nose", "naak band"],
                "advice": "Patient reports cold. Advise: Rest, warm fluids, steam inhalation, Vitamin C. Usually resolves in 7-10 days. If symptoms worsen, consult doctor.",
                "questions": ["Any fever with cold?", "How many days have you had cold?"]
            },
            # Headache related
            "headache": {
                "keywords": ["headache", "sir dard", "sar dard", "migraine", "head pain", "sir me dard"],
                "advice": "Patient reports headache. Advise: Rest in dark room, stay hydrated, take paracetamol if needed. If severe, sudden, or with vision changes, seek emergency care.",
                "questions": ["Where exactly is the pain?", "How severe on scale of 1-10?", "Any nausea or vision problems?"]
            },
            # Stomach related
            "stomach": {
                "keywords": ["stomach", "pet", "pet dard", "acidity", "gas", "diarrhea", "dast", "loose motion", "vomiting", "ulti", "nausea"],
                "advice": "Patient reports stomach issues. Advise: ORS for dehydration, bland BRAT diet (banana, rice, apple, toast), avoid spicy food. If blood in stool or severe pain, seek immediate care.",
                "questions": ["Any vomiting or loose motions?", "How many times?", "Any blood in stool?"]
            },
            # Body pain
            "body_pain": {
                "keywords": ["body pain", "badan dard", "joint pain", "jodo me dard", "muscle pain", "weakness", "kamzori"],
                "advice": "Patient reports body pain. Advise: Rest, warm compress, gentle stretching. If fever accompanies, could be viral. Persistent pain needs doctor visit.",
                "questions": ["Any fever with body pain?", "Which area hurts most?", "Did you do any heavy work recently?"]
            },
            # Breathing issues
            "breathing": {
                "keywords": ["breathing", "saans", "breath", "shortness", "difficulty breathing", "saans phoolna", "asthma", "dama"],
                "advice": "ATTENTION: Patient reports breathing difficulty. This could be serious. Advise: Sit upright, use inhaler if prescribed. If severe, SEEK EMERGENCY CARE IMMEDIATELY.",
                "questions": ["How severe is breathing difficulty?", "Any chest pain?", "Do you have asthma or heart condition?"],
                "priority": "HIGH"
            },
            # Chest pain
            "chest": {
                "keywords": ["chest pain", "seene me dard", "heart", "dil", "chest tightness"],
                "advice": "CRITICAL: Patient reports chest pain. Could be cardiac. ADVISE IMMEDIATE EMERGENCY CARE. Ask to chew aspirin if available and not allergic.",
                "questions": ["Does pain radiate to arm or jaw?", "Any sweating?", "Difficulty breathing?"],
                "priority": "CRITICAL"
            },
            # Diabetes symptoms
            "diabetes": {
                "keywords": ["sugar", "diabetes", "thirst", "pyas", "frequent urination", "baar baar peshaab", "weakness"],
                "advice": "Patient shows diabetes-related symptoms. Advise: Get blood sugar tested. If diabetic, check current sugar levels. Avoid sweets, stay hydrated.",
                "questions": ["Do you have diabetes?", "When did you last check sugar levels?", "Any unusual thirst or urination?"]
            },
            # BP related
            "bp": {
                "keywords": ["bp", "blood pressure", "high bp", "low bp", "dizzy", "chakkar", "giddiness"],
                "advice": "Patient shows BP-related symptoms. Advise: Sit/lie down if dizzy, check BP if meter available. Avoid sudden movements. If severe headache or chest pain, seek immediate care.",
                "questions": ["Do you have BP history?", "What was last BP reading?", "Taking BP medications?"]
            }
        }

        self.detected_symptoms = []
        self.advice_context = ""
        self.priority = "NORMAL"

    def analyze(self, transcript: str) -> dict:
        """
        Analyzes transcript for symptoms and generates medical advice context.
        Returns: dict with detected symptoms, advice, and suggested questions
        """
        text = transcript.lower()
        self.detected_symptoms = []
        advice_parts = []
        questions = []
        self.priority = "NORMAL"

        for symptom_name, symptom_data in self.symptom_database.items():
            if any(keyword in text for keyword in symptom_data["keywords"]):
                self.detected_symptoms.append(symptom_name)
                advice_parts.append(symptom_data["advice"])
                questions.extend(symptom_data.get("questions", []))
                
                # Check priority
                if symptom_data.get("priority") == "CRITICAL":
                    self.priority = "CRITICAL"
                elif symptom_data.get("priority") == "HIGH" and self.priority != "CRITICAL":
                    self.priority = "HIGH"

        if self.detected_symptoms:
            self.advice_context = "\n".join(advice_parts)
            return {
                "symptoms_detected": self.detected_symptoms,
                "medical_advice": self.advice_context,
                "follow_up_questions": questions[:3],  # Limit to 3 questions
                "priority": self.priority,
                "has_symptoms": True
            }

        return {
            "symptoms_detected": [],
            "medical_advice": "",
            "follow_up_questions": [],
            "priority": "NORMAL",
            "has_symptoms": False
        }

    def get_llm_context(self) -> str:
        """
        Returns formatted context for LLM to generate appropriate response.
        """
        if not self.detected_symptoms:
            return ""

        context = f"""
PATIENT SYMPTOM REPORT:
Detected Symptoms: {', '.join(self.detected_symptoms)}
Priority Level: {self.priority}

MEDICAL GUIDANCE TO PROVIDE:
{self.advice_context}

INSTRUCTIONS FOR RESPONSE:
- Be empathetic and reassuring
- Provide specific home remedies that can help
- Mention warning signs when to seek immediate care
- If priority is CRITICAL or HIGH, emphasize urgency
- Keep response conversational in Hinglish
- Mention that you'll note this in their health record
"""
        return context

    def reset(self):
        """Reset agent state for new conversation."""
        self.detected_symptoms = []
        self.advice_context = ""
        self.priority = "NORMAL"
