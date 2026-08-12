import os
import time
import requests

OKTA_DOMAIN = "https://trial-1602807.okta.com"

# GitHub safely injects your secret token into environment variables
API_TOKEN = os.environ.get("OKTA_API_TOKEN")

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"SSWS {API_TOKEN}"
}

def generate_okta_logs(count=10):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Generating Okta API logs via GitHub Actions...")

    endpoints = [
        "/api/v1/users?limit=1",
        "/api/v1/apps?limit=1",
        "/api/v1/groups?limit=1",
        "/api/v1/authorizationServers",
        "/api/v1/zones",
        "/api/v1/policies?type=OKTA_SIGN_ON",
        "/api/v1/authenticators",
        "/api/v1/brands",
        "/api/v1/eventHooks",
        "/api/v1/inlineHooks"
    ]

    for index, endpoint in enumerate(endpoints[:count], start=1):
        url = f"{OKTA_DOMAIN}{endpoint}"
        try:
            response = requests.get(url, headers=headers)
            print(f"  ({index}/{count}) Endpoint: {endpoint} | Status: {response.status_code}")
        except Exception as e:
            print(f"  ({index}/{count}) Error calling {endpoint}: {e}")

        time.sleep(1)

if __name__ == "__main__":
    generate_okta_logs(10)
