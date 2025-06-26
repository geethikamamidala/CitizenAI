import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WATSONX_APIKEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
MODEL_ID = os.getenv("WATSONX_MODEL_ID")
WATSONX_URL = os.getenv("WATSONX_URL")

def get_granite_response(prompt):
    # Get IAM token
    token_res = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if token_res.status_code != 200:
        print("Auth Error:", token_res.text)
        return "Error authenticating with IBM Watson"

    access_token = token_res.json().get("access_token")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": MODEL_ID,
        "project_id": PROJECT_ID,
        "input": prompt,
        "parameters": {
            "max_new_tokens": 1024
        }
    }

    endpoint = f"{WATSONX_URL}/ml/v1/text/generation?version=2024-05-01"
    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["results"][0]["generated_text"]
    else:
        print("Watsonx Error:", response.status_code, response.text)
        return "Error contacting IBM Granite API"
