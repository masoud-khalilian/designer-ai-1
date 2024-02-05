import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from config import config_prompt as cfg_p
from src.strict_text_formatting import strict_text
from src.tools import process_json
from src.er_model import ErModel
from src.array_generator import ArrayGenerator

# this function will run the program with pre maide response from the server
# it basically starts from second part of the programm
# the pre made er respnse is saved at api-er-response.txt


def main():
    load_dotenv()
    open_api_key = os.getenv("API_KEY")
    client = OpenAI(api_key=open_api_key)

    file_path = 'api-er-response.txt'
    with open(file_path, 'r') as file:
        saved_respose = file.read()

    pre_er_model = ErModel(saved_respose)
    er3 = pre_er_model.get_model()
    er_model = ErModel(er3)
    generator = ArrayGenerator(er3)
    json_array = generator.get_transformed_array()

    python_list = json_array.tolist()
    json_string = json.dumps(python_list)
    res = json.loads(json_string)
    res = list(filter(lambda x: x is not None, res))
    er_model.save_model(res, file_name=f"er_model_manual")

    print(f"JOB local SUCCESSFULLY DONE !!!\n")


if __name__ == "__main__":
    main()
