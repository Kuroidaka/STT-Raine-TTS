import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def search(q):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
    "q": q
    })
    headers = {
    'X-API-KEY': os.environ['SERPER_API_KEY'],
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

print(search("who is the viet name president"))