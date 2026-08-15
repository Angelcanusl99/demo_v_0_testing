import requests

BASE_URL = "http://127.0.0.1:8000/api/prototypes"

print("Starting Canus client tests...\n")

print("--- 1. REQUESTING INVENTORY (GET) ---")
get_response = requests.get(BASE_URL)

print(f"Status code: {get_response.status_code}")
print(f"Data received: {get_response.json()}\n")

print("--- 2. REGISTERING NEW MODEL (POST) ---")
new_prototype_data = {
    "model_name": "Canus-Omega",
    "engine_type": "Hydrogen",
    "horsepower": 1200,
    "weight": 1150.0
}
post_response = requests.post(BASE_URL, json=new_prototype_data)

print(f"Status code: {post_response.status_code}")
print(f"Server response: {post_response.json()}\n")

print("--- 3. UPDATING HORSEPOWER (PUT) ---")
put_url = f"{BASE_URL}/1"
put_response = requests.put(put_url, params={"new_hp": 950})

print(f"Status code: {put_response.status_code}")
print(f"Server response: {put_response.json()}\n")
