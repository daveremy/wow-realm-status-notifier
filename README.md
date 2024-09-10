# WoW Realm Status Notifier

A Python script that monitors the status of a specific World of Warcraft realm (e.g., Area 52) and notifies the user when the server is back online. The script uses the Blizzard API to check the server status and can be expanded to send notifications via email or SMS.

## Features

- Fetches the status of a specified WoW realm using the Blizzard API.
- Uses OAuth 2.0 for authentication with Blizzard's API.
- Keeps your Blizzard API credentials secure using environment variables.

## Setup Instructions

### Prerequisites

- **Python 3.x**: Make sure Python is installed on your system.
- **Blizzard Developer Account**: You'll need to [create an account](https://develop.battle.net/) and register an application to get a `Client ID` and `Client Secret`.
- **Dependencies**: Install the required Python packages (listed below).

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/daveremy/wow-realm-status-notifier.git
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

5. Add your Blizzard API credentials to the `.env` file:

    ```bash
    CLIENT_ID=your_actual_client_id
    CLIENT
