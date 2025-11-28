import json
from groq import AsyncGroq
from app.core.exceptions import LLMError, ConfigurationError
from app.core.config import settings


class GroqService:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ConfigurationError("GROQ_API_KEY is missing in .env file")

        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)

        try:
            with open("assets/medical_facts.json", "r") as f:
                self.knowledge_graph = json.load(f)
                self.facts_str = json.dumps(self.knowledge_graph, indent=2)
        except:
            self.facts_str = "Standard Emergency Protocols Apply."

    async def extract_profile_data(self, user_text: str, required_fields: list) -> dict:
        """
        Robust Data Extraction (Non-Streaming)
        """
        fields_str = ", ".join(required_fields)
        extraction_prompt = f"""
        You are a strict Data Entry API. 
        Extract specific values from the user's speech into JSON.
        
        TARGET FIELDS: [{fields_str}]
        
        CRITICAL RULES:
        1. EXTRACT ONLY WHAT IS EXPLICITLY STATED. DO NOT GUESS.
        2. If the user does not mention a value, return null. 
        3. 'No'/'Healthy' -> condition: 'Healthy'.
        
        INPUT: "{user_text}"
        
        OUTPUT JSON ONLY.
        """
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": extraction_prompt},
                    {"role": "user", "content": user_text},
                ],
                model="llama-3.1-8b-instant",
                temperature=0.0,
                max_tokens=200,
                response_format={"type": "json_object"},
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            print(f"Extraction Error: {e}")
            return {}

    async def generate_response(self, user_input, context: str = "", is_symptom_consultation: bool = False) -> tuple[str, str]:
        text_input = user_input
        if isinstance(user_input, list):
            text_input = user_input[0]["text"] if user_input else ""

        # Enhanced prompt for symptom consultation
        if is_symptom_consultation:
            system_prompt = f"""
            You are Arogya, a warm and knowledgeable AI Medical Doctor for rural India.
            
            PATIENT CONTEXT:
            {context}
            
            MEDICAL KNOWLEDGE:
            {self.facts_str}

            YOUR ROLE AS A DOCTOR:
            1. **Listen with empathy**: Acknowledge the patient's suffering first.
            2. **Provide clear medical advice**: Give specific home remedies and care instructions.
            3. **Mention warning signs**: Tell them when to seek hospital care.
            4. **Be conversational**: Use Hinglish naturally, like a caring village doctor.
            5. **Keep it focused**: 3-4 sentences maximum with actionable advice.
            
            RESPONSE STYLE:
            - Start with acknowledgment: "Haan, bukhar aur khansi hai toh..."
            - Give specific remedies: warm water, honey, rest, medicines
            - End with reassurance or warning if needed
            
            OUTPUT FORMAT:
            [REASONING]: <Your medical assessment>
            [RESPONSE]: <What you say to patient - warm, helpful, doctor-like>
            """
        else:
            system_prompt = f"""
            You are Arogya, an empathetic AI Medical Assistant for rural India.
            CONTEXT: {context}
            KNOWLEDGE: {self.facts_str}

            INSTRUCTIONS:
            1. **Reasoning First**: Think about the medical implication first.
            2. **Hinglish Output**: Speak naturally and respectfully.
            3. **Concise**: Keep response under 2 sentences.
            4. **CRITICAL SAFETY RULE**: If the user is currently UNREGISTERED (Onboarding mode), your SOLE priority is to complete the missing patient data. Do NOT provide medical advice or divert from the data goal.
            
            OUTPUT FORMAT:
            [REASONING]: <Medical thought process>
            [RESPONSE]: <Actual speech>
            """

        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User: {text_input}"},
                ],
                model="llama-3.1-8b-instant",
                temperature=0.3,
                max_tokens=250,
            )

            raw_content = chat_completion.choices[0].message.content
            reasoning = "Analysis Complete"
            response = raw_content

            if "[RESPONSE]:" in raw_content:
                parts = raw_content.split("[RESPONSE]:")
                reasoning = (
                    parts[0]
                    .replace("[REASONING]:", "")
                    .replace("[RESPONSE]:", "")
                    .strip()
                )
                if len(parts) > 1:
                    response = parts[1].strip()

            return reasoning, response

        except Exception as e:
            print(f"Groq Error: {e}")
            return "Error", "Maaf kijiye, main sun nahi paayi."
