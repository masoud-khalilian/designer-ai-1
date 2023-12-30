import os
from dotenv import load_dotenv
from openai import OpenAI

from src.er_model import ErModel
from src.prompt import Prompt
from src.module import Process

class CallOpenAI(Process):
    def __init__(self,prompt='',system_prompt=''):
        super().__init__('call open ai api')
        load_dotenv()
        self.open_api_key = os.getenv("API_KEY")
        self.prompt = prompt
        self.response = ''
        self.answer = ''
        self.system_prompt = system_prompt

    def __call__(self):

        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.open_api_key,
        )
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f'{self.system_prompt}'},
                {"role": "user", "content": f'{self.prompt}'}
            ],
            model="gpt-3.5-turbo-1106",
            )
        self.response = completion.choices[0].message
        self.answer = completion.choices[0].message.content
        return completion.choices[0].message.content