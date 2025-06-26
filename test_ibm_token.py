import requests
import os

API_KEY = "XHBLRsfHq_OJqLkrz4e3uBSHAQFQC5bodAyDjh3XT2ZJ"

response = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

print("Status:", response.status_code)
print("Response:", response.text)
