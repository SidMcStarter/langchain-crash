import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def scrape_from_linkedin(url, mock=False):
    if mock:
        result = requests.get("https://gist.githubusercontent.com/SidMcStarter/387067dffaa60130c8f35735ab5d535e/raw/9ee69afdd4fc4aeead519cb0593f4d08e487c43c/sdileep-link.json")
    else:
        api_endpoint = "https://api.scrapin.io/v1/enrichment/profile"
        params = {
            "linkedInUrl": url,
            "apikey": os.getenv("SCRAPIN_API_KEY")
        }
        result = requests.get(api_endpoint, params=params)
        if result.status_code == 200:
            with open("linkedin_data.json", "w") as file:
                file.write(result.text)
        else:
            raise Exception(f"Error fetching data from LinkedIn: {result.status_code} - {result.text}")
    result = {
        k:v
        for k, v in result.json().items()
        if k not in ["certifications"] and v not in ["", None, []]
    }
    if "person" in result:
        result = result["person"]
    return result
    