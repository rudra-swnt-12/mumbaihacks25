class CheckinAgent:
    def __init__(self):
        self.symptom_flags = {"thirst": False, "urination": False, "hunger": False}
        self.checklist = {"medication": False, "symptoms": False, "diet": False}
        self.current_focus = "medication"
        self.is_complete = False

    def _update_symptoms(self, text: str):
        """
        Processes text for 3 Ps and simple negation.
        """
        if "not" in text or "nahi" in text or "no" in text:
            return

        if any(
            keyword in text
            for keyword in ["pyaas", "thirst", "zyada pani", "more water"]
        ):
            self.symptom_flags["thirst"] = True

        if any(
            keyword in text for keyword in ["toilet", "bathroom", "bar bar", "often"]
        ):
            self.symptom_flags["urination"] = True

        if any(keyword in text for keyword in ["bhukh", "hunger", "zyada khana"]):
            self.symptom_flags["hunger"] = True

        if any(keyword in text for keyword in ["dawa", "pill", "goli"]):
            self.checklist["medication"] = True

        if self.symptom_flags["thirst"] or self.symptom_flags["urination"]:
            self.checklist["symptoms"] = True

        if any(keyword in text for keyword in ["khana", "food", "roti", "rice"]):
            self.checklist["diet"] = True

    def get_risk_score(self) -> str:
        """
        Performs Clinical Triangulation to infer risk based on symptoms.
        This output goes directly to the LLM context.
        """
        s = self.symptom_flags

        if s["thirst"] and s["urination"]:
            return "CLINICAL_RISK_HIGH"

        if s["thirst"] or s["urination"]:
            return "CLINICAL_RISK_MODERATE"

        return "CLINICAL_RISK_LOW"

    def determine_next_move(self, transcript: str, med_status: dict) -> str:
        """
        This function no longer dictates the exact question.
        It provides the LLM with the current STATUS for intelligent response generation.
        """
        text = transcript.lower()

        self._update_symptoms(text)
        if all(self.checklist.values()):
            self.is_complete = True
            return "All routine checks complete. Focus on any new patient symptoms."

        if not self.checklist["medication"]:
            self.current_focus = "medication"
            return "URGENTLY need to confirm medication adherence (Did they take their pill?)."

        if not self.checklist["symptoms"]:
            self.current_focus = "symptoms"
            return "NEED TO CHECK 3 Ps VITAL SIGNS (Thirst/Urination frequency)."

        if not self.checklist["diet"]:
            self.current_focus = "diet"
            return "NEED TO CONFIRM BREAKFAST DETAILS for full daily log."

        return "Routine check complete. Triage the patient's current symptoms."
