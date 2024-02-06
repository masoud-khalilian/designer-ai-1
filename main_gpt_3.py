import json
from src.array_generator import ArrayGenerator
from src.api_module import Call_Api
from src.prompt import Prompt
from src.pre_processing_module import RemoveSpace, PromptGeneration
from config import config_prompt as cfg
from src.tools import log_preliminary_er
from src.er_model import ErModel


def main():

    output_file_name = "er_model"
    prompt_overhead = "As er model designer design this explaination: "
    system_propmt = cfg.system_1_manual.value
    temperature = 0.01

    print("Welcome to Designer AI 1")
    init_prompt = Prompt()
    init_prompt.get_input()

    _remove_space = RemoveSpace()
    _pre_overhead = PromptGeneration(name='prompt 1', overhead=prompt_overhead)
    init_prompt.execute_module(_remove_space)
    init_prompt.execute_module(_pre_overhead)

    call_api = Call_Api()

    preliminary_er = call_api.call_gpt3(prompt=init_prompt.get_prompt(),
                                        system_prompt=system_propmt,
                                        custom_model="ft:gpt-3.5-turbo-1106:personal::8eTGxlAz",
                                        temperature=temperature)

    log_preliminary_er(preliminary_er, "preliminary_er_GPT3")

    pre_er_model = ErModel(preliminary_er)
    er3 = pre_er_model.get_model()
    er_model = ErModel(er3)
    generator = ArrayGenerator(er3)
    json_array = generator.get_transformed_array()

    python_list = json_array.tolist()
    json_string = json.dumps(python_list)
    res = json.loads(json_string)
    res = list(filter(lambda x: x is not None, res))
    er_model.save_model(res, file_name=output_file_name)

    print(f"JOB SUCCESSFULLY DONE !!!\n")


if __name__ == "__main__":
    main()
