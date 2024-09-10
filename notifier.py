import os
import time
import requests
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Blizzard API credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://us.battle.net/oauth/token"

# Pushover credentials from environment variables
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

# Global variable for realms to monitor (use connected realm ID)
REALMS_TO_MONITOR = [
    # Add realm name and connected realm ID here
    {"name": "Area 52", "id": 3676, "last_status": None},
    # {"name": "Stormrage", "id": 1234, "last_status": None},  # Example
]


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


def send_pushover_notification(message, title="WoW Realm Status", priority=1):
    """Send a push notification using Pushover with high priority."""
    payload = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "title": title,
        "priority": priority,  # Always high priority
    }
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json", data=payload)
        response.raise_for_status()
        print(f"Push notification sent with priority {priority}.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send push notification: {e}")


def check_connected_realm_status(access_token, realm):
    """Check the status of the connected WoW realm using the access token."""
    connected_realm_url = f"https://us.api.blizzard.com/data/wow/connected-realm/{realm['id']}?namespace=dynamic-us&locale=en_US"
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    try:
        response = requests.get(connected_realm_url, headers=headers)
        response.raise_for_status()
        connected_realm_data = response.json()

        # Check the detailed realm status
        status_type = connected_realm_data['status']['type']

        # Only send notifications if the status has changed
        if status_type != realm["last_status"]:
            realm["last_status"] = status_type
            if status_type == 'UP':
                print(Fore.GREEN +
                      f"The connected realm {realm['name']} is online!")
                send_pushover_notification(
                    f"WoW Realm {realm['name']} is Online! The realm is back online and available."
                )
            else:
                print(
                    Fore.RED + f"The connected realm {realm['name']} is offline or having issues.")
                send_pushover_notification(
                    f"WoW Realm {realm['name']} is Offline. The realm is currently down or having issues."
                )
        else:
            # If the status hasn't changed, we don't notify.
            print(
                Fore.YELLOW + f"No status change for realm {realm['name']}. Status is still {status_type}.")
    except requests.exceptions.RequestException as e:
        print(f"Error checking realm status for {realm['name']}: {e}")


def monitor_realms():
    """Monitor the list of realms and check their status."""
    print(Style.BRIGHT + Fore.CYAN +
          "Monitoring the following WoW realms (press Ctrl+C to exit):")
    for realm in REALMS_TO_MONITOR:
        print(Fore.CYAN + f"- {realm['name']} (ID: {realm['id']})")

    # Step 1: Get an access token
    token = get_access_token()

    if token:
        try:
            # Step 2: Keep checking the realm status every 5 minutes and send notifications
            while True:
                for realm in REALMS_TO_MONITOR:
                    check_connected_realm_status(token, realm)
                time.sleep(300)  # Wait 5 minutes before checking again
        except KeyboardInterrupt:
            print(Fore.BLUE + "\nExiting program gracefully. Goodbye!")
    else:
        print(Fore.RED + "Failed to get access token. Exiting.")


if __name__ == "__main__":
    monitor_realms()
