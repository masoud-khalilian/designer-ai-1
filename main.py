from src.er_model import ErModel
from src.api_module import CallOpenAI
from src.prompt import Prompt
from src.pre_processing_module import RemoveSpace, PromptGeneration  # ,Summarize
from config import config_prompt as cfg


def main():
    print("Welcome to Designer-ai-1 !!!")
    init_prompt = Prompt()
    init_prompt.get_input()

    _remove_space = RemoveSpace()
    _pre_overhead = PromptGeneration(
        name='prompt generation 1', overhead=cfg.user_1.value)

    init_prompt.execute_module(_remove_space)
    init_prompt.execute_module(_pre_overhead)
    print('We have got your prompt we are going to send it to our llm to get preliminary ER.')
    preliminary_er = CallOpenAI(
        prompt=init_prompt.get_prompt(), system_prompt=cfg.system_1.value)()
    print('We have recieved your preliminary ER from the llm.')
    pre_er_model = ErModel(preliminary_er)

    pre_er_model.display_model()
    second_prompt = Prompt(pre_er_model.get_model())

    generation2 = PromptGeneration(name='prompt generation 2')
    output_format_prompt = generation2.indicate_format()

    print('We prepared prelimnary er and our json format. Now we ask llm to give us the array.')

    json_array = CallOpenAI(prompt=second_prompt.get_prompt(),
                            system_prompt=cfg.api_call_system2.value + output_format_prompt)()

    print('We have got an array from the llm now we are going to parse it so you can upload it to website.')

    er_model = ErModel(json_array)
    er_model.save_model(cfg.strict_format.value)
    print("JOB SUCCESSFULLY DONE !!!")
    print("please upload the file called ER_model_final_response.json and tell us it worked properly or not.")


if __name__ == "__main__":
    main()
