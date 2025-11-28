import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.checkin_agent import CheckinAgent


def test_checkin_flow():
    print("📋 --- TESTING CHECKIN AGENT LOGIC ---")

    # Initialize the Agent
    agent = CheckinAgent()

    # Simulate medication state (Assume false initially)
    fake_med_state = {"morning_meds_taken": False}

    # --- TURN 1: Start of call ---
    print("\n[Turn 1] User: 'Hello'")
    # The agent should see that 'medication' is False in the checklist
    action = agent.determine_next_move("Hello", fake_med_state)
    print(f"   👉 AI Agenda: {action}")

    if "Medication" in action:
        print("   ✅ Correct: Agent asked about Medication.")
    else:
        print("   ❌ Error: Agent failed to ask about Medication.")

    # --- TURN 2: User confirms meds ---
    print("\n[Turn 2] User: 'Haan dawai kha li' (Yes took meds)")
    # The agent checks the transcript, sees "dawai" + "kha li", updates checklist
    action = agent.determine_next_move("Haan dawai kha li", fake_med_state)
    print(f"   👉 AI Agenda: {action}")

    if "Vitals" in action or "Symptoms" in action:
        print("   ✅ Correct: Agent moved to Symptoms.")
    else:
        print(f"   ❌ Error: Agent stayed on {action}")

    # --- TURN 3: User confirms symptoms ---
    print(
        "\n[Turn 3] User: 'Main theek hoon, koi chakkar nahi' (I am fine, no dizziness)"
    )
    # The agent sees "theek" or "chakkar", updates checklist
    action = agent.determine_next_move("Main theek hoon", fake_med_state)
    print(f"   👉 AI Agenda: {action}")

    if "Diet" in action:
        print("   ✅ Correct: Agent moved to Diet.")
    else:
        print(f"   ❌ Error: Agent stayed on {action}")

    # --- TURN 4: User confirms diet ---
    print("\n[Turn 4] User: 'Maine roti sabzi khayi'")
    # The agent sees "roti", updates checklist
    action = agent.determine_next_move("Maine roti sabzi khayi", fake_med_state)
    print(f"   👉 AI Agenda: {action}")

    if "Complete" in action:
        print("   ✅ Correct: Agent finished the check-in.")
    else:
        print(f"   ❌ Error: Agent did not finish. Got: {action}")

    print("\n✅ LOGIC TEST COMPLETE.")


if __name__ == "__main__":
    test_checkin_flow()
