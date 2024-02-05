import json
from codelama_array_generator import CustomArrayGenerator
from src.api_module import Call_Api
from src.prompt import Prompt
from src.pre_processing_module import RemoveSpace, PromptGeneration  # ,Summarize

from config import config_prompt as cfg
from config import config_model as cfg_model
from src.tools import log_preliminary_er

from src.er_model import ErModel


def main():

    model_name = cfg_model.gemini.value
    prompt_overhead = cfg.code_lama_prompt_overhead.value

    print("Welcome to Designer-ai-1 !!!")
    init_prompt = Prompt()
    init_prompt.get_input()

    _remove_space = RemoveSpace()
    _pre_overhead = PromptGeneration(name='prompt 1', overhead=prompt_overhead)
    init_prompt.execute_module(_remove_space)
    init_prompt.execute_module(_pre_overhead)

    call_api = Call_Api()
    preliminary_er = call_api.call_open_router(model_name=model_name,
                                               prompt=init_prompt.get_prompt())
    log_preliminary_er(preliminary_er, model_name)

    pre_er_model = ErModel(preliminary_er)
    er3 = pre_er_model.get_model()
    er_model = ErModel(er3)
    generator = CustomArrayGenerator(er3)
    json_array = generator.get_transformed_array()

    python_list = json_array.tolist()
    json_string = json.dumps(python_list)
    res = json.loads(json_string)
    res = list(filter(lambda x: x is not None, res))
    er_model.save_model(res, file_name=f"er_model_manual")

    print(f"JOB SUCCESSFULLY DONE !!!\n")


if __name__ == "__main__":
    main()
