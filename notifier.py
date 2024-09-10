import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Blizzard API credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://us.battle.net/oauth/token"

# WoW Connected Realm API endpoint
REGION = "us"
CONNECTED_REALM_ID = 3676  # The connected realm ID for Area 52
CONNECTED_REALM_URL = f"https://{REGION}.api.blizzard.com/data/wow/connected-realm/{CONNECTED_REALM_ID}?namespace=dynamic-{REGION}&locale=en_US"


def get_access_token():
    """Fetch an OAuth access token from Blizzard."""
    try:
        response = requests.post(TOKEN_URL, data={
            'grant_type': 'client_credentials'
        }, auth=(CLIENT_ID, CLIENT_SECRET))

        response.raise_for_status()
        token_data = response.json()
        return token_data['access_token']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching access token: {e}")
        return None


def check_connected_realm_status(access_token):
    """Check the status of the connected WoW realm using the access token."""
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    try:
        response = requests.get(CONNECTED_REALM_URL, headers=headers)
        response.raise_for_status()
        connected_realm_data = response.json()

        # Print the connected realm status
        print(connected_realm_data)

        # Check the detailed realm status
        if connected_realm_data['status']['type'] == 'UP':
            print(
                f"The connected realm {CONNECTED_REALM_ID} (Area 52) is online!")
        else:
            print(
                f"The connected realm {CONNECTED_REALM_ID} (Area 52) is offline or having issues.")
    except requests.exceptions.RequestException as e:
        print(f"Error checking connected realm status: {e}")


if __name__ == "__main__":
    # Step 1: Get an access token
    token = get_access_token()
    if token:
        # Step 2: Check connected realm status with the access token
        check_connected_realm_status(token)
