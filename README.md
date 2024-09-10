# WoW Realm Status Notifier

A Python script that monitors the status of specific World of Warcraft realms (e.g., Area 52) and sends real-time notifications using Pushover when the server status changes.

## Features

- Fetches the status of specified WoW realms using Blizzard's API.
- Sends high-priority push notifications via Pushover when a realm goes offline or comes back online.
- Configurable list of realms to monitor by name and connected realm ID.
- Graceful exit with Ctrl+C.

## Setup Instructions

### Prerequisites

- **Python 3.x**: Ensure Python is installed on your system.
- **Blizzard Developer Account**: [Create an account](https://develop.battle.net/) and register an application to get a `Client ID` and `Client Secret`.
- **Pushover Account**: [Create an account](https://pushover.net/) and get your `User Key` and `API Token`.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/wow-realm-status-notifier.git
    cd wow-realm-status-notifier
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of the project:

    ```bash
    touch .env
    ```

5. Add your Blizzard and Pushover credentials to the `.env` file:

    ```bash
    CLIENT_ID=your_actual_client_id
    CLIENT_SECRET=your_actual_client_secret
    PUSHOVER_USER_KEY=your_pushover_user_key
    PUSHOVER_API_TOKEN=your_pushover_api_token
    ```

### Running the Script

1. Configure the `REALMS_TO_MONITOR` list in the script with the realm name and its connected realm ID. For example:

    ```python
    REALMS_TO_MONITOR = [
        {"name": "Area 52", "id": 3676, "last_status": None},
    ]
    ```

   You can find the connected realm ID for other realms by following the instructions in the next section.

2. Run the notifier script:

    ```bash
    python notifier.py
    ```

   The script will print which realms are being monitored and check their status every 5 minutes. It will send a **high-priority notification** via Pushover whenever a realm goes offline or comes back online.

   To exit the script, press **Ctrl+C** to exit gracefully.

## How to Find the Connected Realm ID

To monitor a specific WoW realm, you need its **connected realm ID**. Here's how to find it:

1. **Use Blizzard's API** to query the realm information:
   
   - Access the [WoW Realm Status API](https://develop.battle.net/documentation/world-of-warcraft/game-data-apis). You can query the realm status using the **realm slug** (a URL-friendly version of the realm name).
   
   - You can access the information by going to the following URL, replacing `realm-slug` with the name of the realm you want to monitor (in lowercase and replacing spaces with dashes):

     ```
     https://us.api.blizzard.com/data/wow/realm/realm-slug?namespace=dynamic-us&locale=en_US&access_token=your_access_token
     ```

   - The **`connected_realm`** object in the response will contain a URL that includes the **connected realm ID**.

2. **Use an Online Database**:

   Some websites provide an easy way to look up realm information without needing to interact with the API directly. Websites like **[WoW Progress](https://www.wowprogress.com/)** and **[Raider.IO](https://raider.io/)** often list realm information, including connected realms.

3. **Example for Area 52**:
   
   For the realm "Area 52", the **connected realm ID** is `3676`. You would use this ID in the `REALMS_TO_MONITOR` list in the script.

---

### Configuration

To monitor multiple realms, update the `REALMS_TO_MONITOR` list in the script. For example:

```python
REALMS_TO_MONITOR = [
    {"name": "Area 52", "id": 3676, "last_status": None},
    {"name": "Stormrage", "id": 1234, "last_status": None},  # Replace with actual connected realm ID
]
```

### License

This project is licensed under the MIT License.