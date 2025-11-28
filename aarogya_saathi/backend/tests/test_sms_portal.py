import requests
import json

# 1. CONFIGURATION
API_URL = "http://127.0.0.1:8000"
# Use the number configured in your .env as NEIGHBOR_PHONE_NUMBER
TEST_PHONE = "+1234567890"


def run_portal_test():
    print("🏥 --- TESTING DOCTOR PORTAL API ---")

    # --- STEP 1: REQUEST OTP ---
    print(f"\n1. Requesting OTP for {TEST_PHONE}...")
    try:
        response = requests.post(
            f"{API_URL}/auth/send-otp", json={"phone_number": TEST_PHONE}
        )

        if response.status_code != 200:
            print(f"❌ Failed to send OTP: {response.text}")
            return

        data = response.json()
        print("✅ OTP Request Successful!")
        print(f"   Response: {data}")

        # In a real app, you'd check your phone.
        # For this test, we extract the 'debug_otp' we added to the backend code.
        received_otp = data.get("debug_otp")
        print(f"🔑 [DEBUG MODE] Extracted OTP: {received_otp}")

        if not received_otp:
            print("❌ Error: No debug_otp returned. Did you update portal.py?")
            return

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    # --- STEP 2: VERIFY OTP ---
    print(f"\n2. Verifying OTP '{received_otp}'...")
    try:
        verify_response = requests.post(
            f"{API_URL}/auth/verify-otp",
            json={"phone_number": TEST_PHONE, "otp": received_otp},
        )

        if verify_response.status_code != 200:
            print(f"❌ Verification Failed: {verify_response.text}")
            return

        # --- STEP 3: VIEW DATA ---
        patient_data = verify_response.json()
        print("✅ ACCESS GRANTED! Here is the Health Snapshot:")
        print(json.dumps(patient_data, indent=2))

    except Exception as e:
        print(f"❌ Verification Error: {e}")


if __name__ == "__main__":
    # Ensure 'requests' is installed: uv add requests
    run_portal_test()
