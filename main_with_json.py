from src.er_model import ErModel
from src.api_module import Call_Api
from src.prompt import Prompt
from src.pre_processing_module import RemoveSpace, PromptGeneration  # ,Summarize
from config import config_prompt as cfg
from src.tools import log_preliminary_er


def main():

    output_file_name = "er_model"
    print("Welcome to Designer AI 1 with Json")

    phase_1_overhead_prompt = cfg.user_1.value
    phase_1_system_prompt = cfg.system_1.value
    phase_2_system_prompt = cfg.api_call_system2.value
    phase_1_temperature = 0.1
    phase_2_temperature = 1  # must be lucky

    init_prompt = Prompt()
    init_prompt.get_input()

    _remove_space = RemoveSpace()
    _pre_overhead = PromptGeneration(
        name='prompt 1', overhead=phase_1_overhead_prompt)
    init_prompt.execute_module(_remove_space)
    init_prompt.execute_module(_pre_overhead)
    print('We have got your prompt we are going to send it to our llm to get preliminary ER.')

    call_api = Call_Api()

    preliminary_er = call_api.call_gpt3(prompt=init_prompt.get_prompt(),
                                        system_prompt=phase_1_system_prompt,
                                        custom_model="ft:gpt-3.5-turbo-1106:personal::8dYiTRrF",
                                        temperature=phase_1_temperature
                                        )

    log_preliminary_er(preliminary_er, "preliminary_er_GPT3")

    print('We have recieved your preliminary ER from the llm.')
    pre_er_model = ErModel(preliminary_er)
    second_prompt = Prompt(pre_er_model.get_model())
    generation2 = PromptGeneration(name='prompt generation 2')
    output_format_prompt = generation2.indicate_format()
    print('We prepared prelimnary er and our json format. Now we ask llm to give us the array.')

    json_array = call_api.call_gpt3(prompt=second_prompt.get_prompt(),
                                    system_prompt=phase_2_system_prompt + output_format_prompt,
                                    custom_model="ft:gpt-3.5-turbo-1106:personal::8dZ284fX",
                                    temperature=phase_2_temperature
                                    )
    print('We have got an array from the llm now we are going to parse it so you can upload it to website.')
    er_model = ErModel(json_array)
    res = er_model.extract_and_convert_to_json()
    er_model.save_model(res, file_name=output_file_name)

    print(f"JOB SUCCESSFULLY DONE !!!")
    print(
        f"please upload the file called {output_file_name}.json and tell us it worked properly or not.")


if __name__ == "__main__":
    main()
