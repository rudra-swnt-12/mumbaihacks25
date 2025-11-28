from app.services.groq_service import GroqService
from rapidfuzz import process, fuzz


class ASRCorrectionService:
    def __init__(self):
        self.groq = GroqService()

        self.valid_medical_terms = [
            "chakkar",
            "pasina",
            "bukhaar",
            "dard",
            "kamzori",
            "thakan",
            "chest",
            "seene",
            "haath",
            "pair",
            "pet",
            "sar",
            "goli",
            "dawa",
            "insulin",
            "sugar",
            "bp",
            "pressure",
            "khansi",
            "sardi",
            "zukam",
            "ultiyan",
            "dast",
            "behoshi",
            "saans",
            "breath",
            "doctor",
            "hospital",
            "ambulance",
        ]

    def _get_phonetic_hints(self, text: str) -> str:
        """
        Scans the raw text for words that sound similar to our medical vocabulary.
        Returns a string of hints for the LLM.
        """
        hints = []
        words = text.split()

        for word in words:
            if len(word) < 3:
                continue

            match = process.extractOne(
                word.lower(),
                self.valid_medical_terms,
                scorer=fuzz.ratio,
                score_cutoff=70,
            )

            if match:
                best_match, score, _ = match
                if best_match != word.lower():
                    hints.append(f"- '{word}' sounds like '{best_match}'")

        return "\n".join(hints)

    async def correct_transcript(
        self, raw_text: str, context: str = "General Medical Triage"
    ) -> str:
        if mode == "IDENTITY":
            return raw_text

        phonetic_hints = self._get_phonetic_hints(raw_text)
        if not phonetic_hints:
            return raw_text
        correction_prompt = f"""
        You are a Semantic Spell Checker for a Medical Bot.
        
        CONTEXT: {context}
        INPUT TEXT: "{raw_text}"
        
        PHONETIC HINTS (Words in the input that sound like medical terms):
        {phonetic_hints}
        
        TASK:
        Review the INPUT TEXT. If a word seems out of place (nonsense), check the PHONETIC HINTS.
        - If the Hint makes more sense in the medical context, REPLACE IT.
        - If the Original word makes sense (e.g. "Test" in "Blood Test"), KEEP IT.
        
        EXAMPLES:
        1. Input: "I have a severe test pain." | Hint: 'test' sounds like 'chest'. -> Output: "I have a severe chest pain."
        2. Input: "I am going for a blood test." | Hint: 'test' sounds like 'chest'. -> Output: "I am going for a blood test."
        
        OUTPUT:
        Return ONLY the corrected sentence.
        """

        try:
            completion = await self.groq.client.chat.completions.create(
                messages=[{"role": "system", "content": correction_prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.0,
                max_tokens=100,
            )
            return completion.choices[0].message.content.strip().replace('"', "")

        except Exception as e:
            print(f"ASR Correction Failed: {e}")
            return raw_text
