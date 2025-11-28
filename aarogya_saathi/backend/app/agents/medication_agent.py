class MedicationAgent:
    def __init__(self):
        self.state = {"morning_meds_taken": False, "last_checked": None}

        self.positive_keywords = [
            "liya",
            "took",
            "kha liya",
            "le liya",
            "done",
            "yes",
            "haan",
        ]
        self.negative_keywords = ["nahi", "forgot", "missed", "no", "bhul", "kal"]
        self.med_keywords = ["dawa", "med", "goli", "pill", "medicine"]

    def process(self, transcript: str):
        """
        Scans text to update medication state.
        Returns: (Status Message for Dashboard, Context Injection for LLM)
        """
        text = transcript.lower()

        is_med_topic = any(word in text for word in self.med_keywords)

        if is_med_topic:
            if any(word in text for word in self.positive_keywords):
                self.state["morning_meds_taken"] = True
                return (
                    "Meds Confirmed",
                    "Patient just confirmed taking medication. Praise them.",
                )
            if any(word in text for word in self.negative_keywords):
                self.state["morning_meds_taken"] = False
                return (
                    "Meds Missed",
                    "Patient missed medication. Gently warn about risks.",
                )

        return None, None

    def get_status(self):
        return self.state
