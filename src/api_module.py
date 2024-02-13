import os
import requests
import json
from dotenv import load_dotenv
from openai import OpenAI

from src.module import Process


class Call_Api(Process):
    def __init__(self):
        super().__init__('call open ai api')
        load_dotenv()
        self.open_api_key = os.getenv("API_KEY")
        self.open_router_api_key = os.getenv("OPEN_ROUTER_KEY_DESGINER")

    def call_gpt3(self, prompt, system_prompt, custom_model="gpt-3.5-turbo-1106", temperature=0.1) -> str:
        client = OpenAI(api_key=self.open_api_key)

        completion = client.chat.completions.create(
            model=custom_model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": f'{system_prompt}'},
                {"role": "user", "content": f'{prompt}'}
            ],
        )
        self.response = completion.choices[0].message
        self.answer = completion.choices[0].message.content
        return completion.choices[0].message.content

    def call_open_router(self, model_name="", prompt="", temperature=0) -> str:
        headers = {
            'Authorization': f'Bearer {self.open_router_api_key}',
        }
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,

            data=json.dumps({
                "model": model_name,  # Optional
                "messages": [
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature
            })
        )
        if response.status_code == 200:
            try:
                json_response = response.json()
                return json_response['choices'][0]['message']['content']
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON response. Error: {e}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        return ''
