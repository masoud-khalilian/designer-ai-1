import os
from dotenv import load_dotenv
from openai import OpenAI

from src.er_model import ErModel
from src.prompt import Prompt
from src.module import Process

# class ApiClient:
#     def __init__(self, base_url):
#         self.base_url = base_url

#     async def _make_request(self, method, endpoint, params=None, data=None, headers=None):
#         url = f"{self.base_url}/{endpoint}"

#         async with httpx.AsyncClient() as client:
#             response = await client.request(method, url, params=params, data=data, headers=headers)

#             if 400 <= response.status_code < 600:
#                 raise ApiError(response.status_code, response.text)

#             return response.json()

#     async def get(self, endpoint, params=None, headers=None):
#         return await self._make_request('GET', endpoint, params=params, headers=headers)

#     async def post(self, endpoint, data=None, headers=None):
#         return await self._make_request('POST', endpoint, data=data, headers=headers)

#     async def put(self, endpoint, data=None, headers=None):
#         return await self._make_request('PUT', endpoint, data=data, headers=headers)

#     async def delete(self, endpoint, headers=None):
#         return await self._make_request('DELETE', endpoint, headers=headers)

# class ApiError(Exception):
#     def __init__(self, status_code, message):
#         self.status_code = status_code
#         self.message = message
#         super().__init__(f"API Error {status_code}: {message}")


class CallOpenAI(Process):
    def __init__(self,overhead=''):
        super().__init__('call open ai api')
        load_dotenv()
        self.open_api_key = os.getenv("API_KEY")
        self.overhead = overhead
        self.response = ''
        self.answer = ''
    
    def __call__(self, er:ErModel):

        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.open_api_key,
        )

        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "This is a description of an database act as a entity relation model guru."},
                {"role": "user", "content": f'{self.overhead} give the answer in less then 60 word'}
            ],
            model="gpt-3.5-turbo",
        )

        # print(completion)
        # print(completion.choices[0].message.content)

        self.response = completion.choices[0].message
        self.answer = completion.choices[0].message.content
        er.set_model(completion.choices[0].message.content)