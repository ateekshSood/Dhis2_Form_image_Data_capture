import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
openrouter_api_key = os.getenv("open_router_api_key")

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + str(openrouter_api_key),
        "Content-Type": "application/json",
    },
    data=json.dumps(
        {
            "model": "google/gemma-4-31b-it:free",
            "messages": [
                {
                    "role": "user",
                    "content": "How many r's are there in word strawberry?",
                }
            ],
            "reasoning": {"enabled": True},
        }
    ),
)

response_text = response.json()

if "error" in response_text:
    print("API Error:", response_text["error"]["metadata"]["raw"])

else:
    response_text = response_text["choices"][0]["message"]["content"]

    print(response_text)



