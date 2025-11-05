# quick_sms.py
from working_sms_sender_bd import WorkingBangladeshiSMSSender
import sys

def quick_start():
    sender = WorkingBangladeshiSMSSender()
    
    if len(sys.argv) > 1:
        phone = sys.argv[1]
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    else:
        phone = input("Enter phone number (01712345678): ")
        count = 10
    
    if sender.validate_bangladeshi_phone(phone):
        print(f"🚀 Sending {count} SMS to {phone}...")
        result = sender.send_bulk_sms(phone, count)
        print(f"✅ Done! Success rate: {result['success_rate']:.1f}%")
    else:
        print("❌ Invalid phone number!")

if __name__ == "__main__":
    quick_start()
