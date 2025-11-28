import json
from app.services.groq_service import GroqService


class SOAPAgent:
    def __init__(self):
        self.groq = GroqService()

    async def generate_report(
        self, conversation_history: list, patient_context: str
    ) -> str:
        """
        Summarizes the call into a medical note JSON.
        """
        transcript_text = "\n".join(conversation_history)

        prompt = f"""
        You are an expert Medical Scribe AI. 
        Your task is to convert a raw Hindi/Hinglish patient conversation into a PROFESSIONAL MEDICAL SOAP NOTE in ENGLISH.

        PATIENT CONTEXT: {patient_context}
        TRANSCRIPT:
        {transcript_text}

        RULES:
        1. TRANSLATE everything to English. Use clinical terms (e.g., "Chakkar" -> "Vertigo/Dizziness", "Sugar" -> "Diabetes").
        2. Format exactly as a JSON object.
        3. Risk Score should be 0 (Healthy) to 100 (Critical Emergency).

        OUTPUT FORMAT:
        {{
        "summary": "SUBJECTIVE: Patient reports [Symptoms]... \\nOBJECTIVE: Detected [Biomarkers/Speech patterns]... \\nASSESSMENT: Likely [Condition]... \\nPLAN: [Action taken, e.g., advised rest/alerted doctor].",
        "risk_score": <int>
        }}
        """

        try:
            completion = await self.groq.client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.1,
                max_tokens=300,
                response_format={"type": "json_object"},
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"SOAP Error: {e}")
            return json.dumps(
                {
                    "summary": f"Error generating note. Transcript length: {len(transcript_text)} chars.",
                    "risk_score": 0,
                }
            )
