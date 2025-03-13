import requests
import base64
import serial
import os
OPENAI_API_KEY = os.getenv["OPENAI_API_KEY"]
IMAGE_PATH = "path/to/your/image"

TypeToNumber = {
    "Biodegradable": 0,
    "Paper": 1,
    "Metal": 2,
    "E-Waste": 3,
    "Plastics": 4,
    "Other": 5
}

def ContentFromJSON(jsondata):
    data = jsondata["choices"][0]["message"]["content"]
    return data

def ImageAnalysis():
    api_key = OPENAI_API_KEY

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    image_path = IMAGE_PATH

    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Give me a ONE WORD ANSWER. Which category should the item on top of the white paper be put into for segregation in garbage? Biodegradable; Paper; Metal; E-Waste; Plastics; Other. ONE WORD ONLY. NO FULLSTOPS Just word."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                    }
                ]
            }
        ],
        "max_tokens": 300
        }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return(response.json())

def NumberToBeFed(TypeOfGarbage):
    return(TypeToNumber[TypeOfGarbage])

