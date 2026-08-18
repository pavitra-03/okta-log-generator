import os
import time
import requests
import random

OKTA_DOMAIN = "https://trial-1602807.okta.com"
# Reads from GitHub Actions Secret (or local environment variable)
API_TOKEN = os.environ.get("OKTA_API_TOKEN")

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"SSWS {API_TOKEN}"
}

def generate_system_logs():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Generating visible Okta System Log events...")

    # Generate a unique temp group name
    random_id = str(random.randint(1000000000, 9999999999))
    group_name = f"Temp_Log_Group_{random_id}"

    # 1. Create Okta Group (Triggers "group.user_group.create" event)
    print(f"  -> Creating group: {group_name}")
    payload = {
        "profile": {
            "name": group_name,
            "description": "Automated log generator test group"
        }
    }
    response = requests.post(f"{OKTA_DOMAIN}/api/v1/groups", headers=headers, json=payload)

    if response.status_code == 200:
        group_id = response.json().get("id")
        print(f"  -> Success! Group ID: {group_id}")
        time.sleep(2)

        # 2. Delete Okta Group (Triggers "group.user_group.delete" event)
        print(f"  -> Cleaning up group: {group_id}")
        delete_res = requests.delete(f"{OKTA_DOMAIN}/api/v1/groups/{group_id}", headers=headers)
        
        if delete_res.status_code == 204:
            print("  -> Cleanup complete.")
        else:
            print(f"  -> Failed to delete group: {delete_res.status_code} - {delete_res.text}")
    else:
        print(f"  -> Failed to create group: {response.status_code} - {response.text}")

    print("Finished! Check Okta System Log UI for group creation/deletion entries.")

if __name__ == "__main__":
    generate_system_logs()
