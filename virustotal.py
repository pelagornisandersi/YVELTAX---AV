import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VT_API_KEY")

def check_hash_virustotal(file_hash):

    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

    headers = {
        "x-apikey": API_KEY
    }

    try:

        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            data = response.json()

            stats = data["data"]["attributes"]["last_analysis_stats"]

            malicious = stats["malicious"]

            suspicious = stats["suspicious"]

            return malicious, suspicious

        else:

            return None

    except:

        return None