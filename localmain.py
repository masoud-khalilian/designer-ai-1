import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from src.er_model import ErModel
from config import config_prompt as cfg_p
from src.strict_text_formatting import strict_text
from src.tools import process_json

# this function will run the program with pre maide response from the server
# it basically starts from second part of the programm
# the pre made er respnse is saved at api-er-response.txt


def main():
    load_dotenv()
    open_api_key = os.getenv("API_KEY")
    client = OpenAI(api_key=open_api_key)

    file_path = 'api-er-response.txt'
    with open(file_path, 'r') as file:
        content = file.read()

    # have a placeholder to dump the response to it
    with open('json_placeholder.json', 'r') as jfile:
        place_holder = json.load(jfile)

    pre_er_model = ErModel()
    pre_er_model.set_model(content)

    strict_text_array_res = strict_text(
        api_clinet=client,
        system_prompt='You are a database designer return a list of object according to this example: ',
        user_prompt=pre_er_model.get_model(),
        output_format=cfg_p.sample_item_array_strict_format.value)

    s1 = strict_text_array_res['itemsArray'].replace('\'', '\"')
    s2 = json.loads(s1)

    place_holder["erDesign"]["model"]["itemsArray"] = s2
    result = process_json(s2)
    place_holder["erDesign"]["model"]["itemsMap"] = result

    with open('ER_model_final_response.json', 'w') as new_file:
        json.dump(place_holder, new_file, indent=2)

    print("JOB SUCCESSFULLY DONE !!!")


if __name__ == "__main__":
    main()
