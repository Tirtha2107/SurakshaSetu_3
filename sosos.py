# from twilio.rest import Client

# account_sid = "AC0267aa0645ac0931c4f0ec308c3a3184"
# auth_token = "343c635b4ae42c7f8bec8eb6de52442b"

# client = Client(account_sid, auth_token)

# # List of VERIFIED phone numbers (trial account)
# numbers = [
#     "+919326940651",
#     "+919082232635",
#     "+919890702128"
# ]

# for number in numbers:
#     try:
#         message = client.messages.create(
#             body="🚨 SOS Alert: I need help! Please contact me immediately.",
#             from_="+17179126294",
#             to=number
#         )
#         print(f"Message sent to {number} | SID: {message.sid}")
#     except Exception as e:
#         print(f"Failed to send to {number}: {e}")




# from twilio.rest import Client
# import time

# account_sid = "AC0267aa0645ac0931c4f0ec308c3a3184"
# auth_token = "343c635b4ae42c7f8bec8eb6de52442b"

# client = Client(account_sid, auth_token)

# from_number = "+17179126294"  # Your Twilio number

# # 4 VERIFIED emergency contact numbers
# numbers = [
#     "+919326940651"
#     "+919890702128",
#     "+919137236391"
# ]

# for number in numbers:
#     try:
#         call = client.calls.create(
#             to=number,
#             from_=from_number,
#             twiml="""
#                 <Response>
#                     <Say voice="alice">
#                         Call from SurakshaSetu
#                         This is an emergency SOS alert.
#                         I need help immediately.
#                         Please contact me as soon as possible.
#                     </Say>
#                 </Response>
#             """
#         )
#         print(f"Call initiated to {number} | SID: {call.sid}")

#         # small delay so Twilio doesn't hit rate limits
#         time.sleep(2)

#     except Exception as e:
#         print(f"Failed to call {number}: {e}")


from twilio.rest import Client
import time

# -------------------------------
# TWILIO CREDENTIALS
# -------------------------------
account_sid = "AC0267aa0645ac0931c4f0ec308c3a3184"
auth_token = "343c635b4ae42c7f8bec8eb6de52442b"

client = Client(account_sid, auth_token)

from_number = "+17179126294"  # Your Twilio phone number

# -------------------------------
# VERIFIED EMERGENCY CONTACTS
# -------------------------------
numbers = [
    "+919326940651"
]

# -------------------------------
# SOS MESSAGE
# -------------------------------
sms_message = (
    "🚨 SOS ALERT from SurakshaSetu 🚨\n"
    "I am in danger and need immediate help.\n"
    "Please contact me ASAP."
)

# -------------------------------
# SEND SMS + CALL
# -------------------------------
for number in numbers:
    try:
        # ---- SEND SMS ----
        sms = client.messages.create(
            to=number,
            from_=from_number,
            body=sms_message
        )
        print(f"SMS sent to {number} | SID: {sms.sid}")

        # ---- MAKE CALL ----
        call = client.calls.create(
            to=number,
            from_=from_number,
            twiml="""
                <Response>
                    <Say voice="alice">
                        Emergency alert from Suraksha Setu.
                        I am in danger and need help immediately.
                        Please contact me as soon as possible.
                    </Say>
                </Response>
            """
        )
        print(f"Call initiated to {number} | SID: {call.sid}")

        # delay to avoid rate limits
        time.sleep(2)

    except Exception as e:
        print(f"Failed for {number}: {e}")
