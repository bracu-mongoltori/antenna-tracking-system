import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGIN_URL = "https://192.168.1.8/api/auth"
DATA_URL = "https://192.168.1.8/signal.cgi"

auth = {
    "username": "ubnt",
    "password": "mt-rover_123"
}

# Create a session (handles cookies automatically)
with requests.Session() as session:
    session.verify = False

    # Login
    response = session.post(LOGIN_URL, data=auth)
    response.raise_for_status()
    print("Logged in")

    # Fetch data continuously
    while True:
        data_response = session.get(DATA_URL)
        data_response.raise_for_status()

        print(data_response.text)

        with open("data.json", "a") as file:
            file.write(data_response.text + "\n")

        time.sleep(1)  # prevent hammering the device
