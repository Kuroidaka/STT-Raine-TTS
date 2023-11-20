from dotenv import load_dotenv
import json
import os
import requests
from bs4 import BeautifulSoup
from summarize import sum

load_dotenv()

def scrape_website(obj, url:str):

    print({"scraping website..."})
    
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }
    
    data = {
        'url': url,
        "elements": [
            {"selector": "a"},
            {"selector": "p"},
            {"selector": "span"},
            {"selector": "h1"},
            {"selector": "h2"},
            {"selector": "h3"},
            {"selector": "h4"},
            {"selector": "h5"},
            {"selector": "h6"},
        ],
        "gotoOptions": {
            "timeout": 10000,
            "waitUntil": "networkidle2"
        }
    }
    
    api_key = os.environ["BROWERLESS_API_KEY"]
    data_json = json.dumps(data)
    list_data = []
    
    post_url = f"https://chrome.browserless.io/scrape?token={api_key}"
    
    response = requests.post(post_url, headers=headers, data=data_json)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        text = json.loads(text)
        for select in text["data"]:
            for data_text in select["results"]:
                if data_text["text"] != "":
                    list_data.append(data_text["text"])
            
        if len(json.dumps(list_data)) > 10000:
            output = sum(obj, json.dumps(list_data))
            print("CONTENTtt:", list_data)
            return output
        else:
            return output
        
    else:
        print("ERROR:", response)
        
        
data_text = scrape_website("what is the news of bitcoin today", "https://news.bitcoin.com/adrian-day-warns-of-inevitable-us-recession-describes-it-as-a-freight-train-heading-towards-us/")

with open("./assets/text/temp.txt", "w") as f:
        f.write(data_text)
        f.close()
