import re


class OnboardingAgent:
    def __init__(self):
        self.profile = {"name": None, "age": None, "condition": None, "location": None}
        self.is_complete = False

    def update_state(self, extracted_data: dict):
        """
        Updates the profile with new data found by the LLM.
        """
        print(f"Updating Profile with: {extracted_data}")

        for key, value in extracted_data.items():
            if key not in self.profile:
                continue

            if value in [None, "Unknown", "null", "None", ""]:
                continue

            if key == "age":
                numbers = re.findall(r"\d+", str(value))
                if numbers:
                    self.profile[key] = int(numbers[0])
            else:
                self.profile[key] = value

        print(f"Current Profile State: {self.profile}")

        if all(v is not None for v in self.profile.values()):
            self.is_complete = True

    def generate_next_instruction(self) -> str:
        """
        Decides what to ask based on missing slots.
        """
        if not self.profile["name"]:
            return "Ask for the patient's full name."

        if not self.profile["age"]:
            return "Ask for the patient's age."

        if not self.profile["location"]:
            return "Ask for the patient's village or city name."

        if not self.profile["condition"]:
            return "Ask if the patient has any existing diseases like Diabetes (Sugar) or BP."

        return (
            "Profile Complete. Thank the user and tell them their Health Card is ready."
        )

    def get_profile(self):
        return self.profile
