import requests

try:
    response = requests.get("http://localhost:8002/ping")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("Failed to connect to the server. Is it running?")
except requests.exceptions.JSONDecodeError:
    print("Server did not return valid JSON.")
