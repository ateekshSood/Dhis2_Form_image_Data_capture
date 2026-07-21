import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
openrouter_api_key = os.getenv("open_router_api_key")

def llm_field_mapping(ocr_text, field_list):

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + str(openrouter_api_key),
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                # "model": "google/gemma-4-31b-it:free",
                "model":"nvidia/nemotron-3-super-120b-a12b:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "analyze the content given to you and map them to the given json_schema and output the response in that order strictly. If you are not sure about a field mapping output low confidence . if you are sure about field mapping ouput high confidence. Strictly only use the dataElementId that are provided in the text content.",
                    },
                    
                    {
                        "role":"user",
                        "content": f"ocr text : {ocr_text} field list : {field_list}"
                    }
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "data_elements",
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "dataElementId": {"type": "string"},
                                    "value": {"type": "string"},
                                    "confidence": {"type": "string", "enum": ["high", "low"]}
                                },
                                "required": ["dataElementId", "value", "confidence"]
                            }
                        },
                        "strict":True
                    }
                },
                "reasoning": {"enabled": True},
            }
        ),
    )
    
    response_text = response.json()
    
    if "error" in response_text:
        raise Exception(response_text["error"]["metadata"]["raw"])
    
    else:
        response_text = response_text["choices"][0]["message"]["content"]
    
        return (json.loads(response_text))


