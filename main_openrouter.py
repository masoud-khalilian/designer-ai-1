import json
from src.array_generator import ArrayGenerator
from src.api_module import Call_Api
from src.prompt import Prompt
from src.pre_processing_module import RemoveSpace, PromptGeneration  # ,Summarize

from config import config_prompt as cfg
from src.tools import log_preliminary_er

from src.er_model import ErModel


def main():
    print("Welcome to Designer-ai-1 !!!")
    init_prompt = Prompt()
    init_prompt.get_input()

    _remove_space = RemoveSpace()
    _pre_overhead = PromptGeneration(
        name='prompt generation 1', overhead=cfg.code_lama2.value)
    init_prompt.execute_module(_remove_space)
    init_prompt.execute_module(_pre_overhead)

    call_api = Call_Api()
    print(init_prompt.get_prompt())
    preliminary_er = call_api.call_open_router(model_name="codellama/codellama-70b-instruct",
                                               prompt=init_prompt.get_prompt())
    print("codellama-70b-instruct", preliminary_er)
    log_preliminary_er(preliminary_er, "code_lama_70b")

    # gpt4 = call_api.call_open_router(model_name="openai/gpt-4",
    #                                  prompt=init_prompt.get_prompt())
    # print("gpt4", gpt4)
    # log_preliminary_er(gpt4, "gpt4")

    # code_lama_34b = call_api.call_open_router(
    #     model_name="meta-llama/codellama-34b-instruct", prompt=init_prompt.get_prompt())
    # print("2 code_lama_34b", code_lama_34b)
    # print("===================================================================================================")
    # print("===================================================================================================")

    # toppy = call_api.call_open_router(
    #     model_name="undi95/toppy-m-7b", prompt=init_prompt.get_prompt())
    # print("3 toppy", toppy)
    # print("===================================================================================================")
    # print("===================================================================================================")

    # open_chat = call_api.call_open_router(
    #     model_name="openchat/openchat-7b", prompt=init_prompt.get_prompt())
    # print("4 open_chat", open_chat)
    # print("===================================================================================================")
    # print("===================================================================================================")

    # zephyr_7b = call_api.call_open_router(
    #     model_name="huggingfaceh4/zephyr-7b-beta", prompt=init_prompt.get_prompt())
    # print("5 zephyr_7b", zephyr_7b)
    # print("===================================================================================================")
    # print("===================================================================================================")

    # mythomax = call_api.call_open_router(
    #     model_name="gryphe/mythomax-l2-13b", prompt=init_prompt.get_prompt())
    # print("6 mythomax", mythomax)
    # print("===================================================================================================")
    # print("===================================================================================================")

    # mixtral = call_api.call_open_router(
    #     model_name="mistralai/mixtral-8x7b-instruct", prompt=init_prompt.get_prompt())
    # print("7 mixtral", mixtral)
    # print("===================================================================================================")
    # print("===================================================================================================")

    # mistralai = call_api.call_open_router(
    #     model_name="mistralai/mistral-medium", prompt=init_prompt.get_prompt())
    # print("8mistralai", mistralai)
    # print("===================================================================================================")
    # print("===================================================================================================")

    # pre_er_model = ErModel(preliminary_er)
    # er3 = pre_er_model.get_model()
    # er_model = ErModel(er3)
    # generator = ArrayGenerator(er3)
    # json_array = generator.get_transformed_array()

    # python_list = json_array.tolist()
    # json_string = json.dumps(python_list)
    # res = json.loads(json_string)
    # res = list(filter(lambda x: x is not None, res))
    # er_model.save_model(res, file_name=f"er_model_manual")

    # print(f"JOB SUCCESSFULLY DONE !!!\n")


if __name__ == "__main__":
    main()
