import os


class TriageAgent:
    def __init__(self):
        self.reflex_map = {
            "dard": "assets/audio_kaha_hai.mp3",
            "pain": "assets/audio_kaha_hai.mp3",
            "dukh": "assets/audio_kaha_hai.mp3",
            "chakkar": "assets/audio_kaha_hai.mp3",
        }

        self.critical_keywords = [
            "chest",
            "heart",
            "breath",
            "bleeding",
            "unconscious",
            "seene",
            "chaati",
            "saans",
            "khoon",
            "behosh",
            "attack",
            "सीने",
            "छाती",
            "सांस",
            "खून",
            "बेहोश",
            "हार्ट अटैक",
        ]

    def check_reflex(self, transcript: str):
        """
        Returns (audio_bytes, keyword, is_hit)
        """
        if not transcript:
            return None, None, False

        text_lower = transcript.lower()

        for keyword, file_path in self.reflex_map.items():
            if keyword in text_lower:
                try:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            return f.read(), keyword, True
                    else:
                        print(f"⚠️ Asset missing: {file_path}")
                except Exception as e:
                    print(f"Reflex Error: {e}")

        return None, None, False

    def analyze_urgency(self, transcript: str) -> dict:
        """Returns context for the LLM"""
        text = transcript.lower()
        for kw in self.critical_keywords:
            if kw in text:
                return {
                    "priority": "CRITICAL",
                    "msg": "Escalate to Hospital immediately",
                }
        return {"priority": "ROUTINE", "msg": "Provide Home Advice"}
