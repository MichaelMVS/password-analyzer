import time
import subprocess
import requests
import json

def test_api():
    print("Starting server test...")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/analyze',
            json={'password': 'MySecureP@ssw0rd123!'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ API is working correctly!\n")
            print("Analysis Results:")
            print(f"  Strength Score: {data['strength_score']}/100")
            print(f"  Strength Label: {data['strength_label']}")
            print(f"  Entropy: {data['entropy']}")
            print(f"  Password Length: {data['password_length']}")
            print(f"  Time to Crack: {data['time_to_crack']['time']}")
            print(f"\nRecommendations:")
            for rec in data['recommendations']:
                print(f"  - {rec}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == '__main__':
    print("Waiting for server to start...")
    time.sleep(3)
    test_api()
