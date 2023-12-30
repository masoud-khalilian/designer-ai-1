from src.er_model import ErModel
from src.api_module import CallOpenAI
from src.prompt import Prompt
from src.pre_processing_module import RemoveSpace, Summarize, PromptGeneration
from config import config_prompt as cfg_p


def main():
    print("Welcome to Designer-ai-1 !!!")
    init_prompt = Prompt()
    pre_er_model = ErModel()
    init_prompt.get_input()

    remove_space = RemoveSpace()
    summarize = Summarize()
    generation1 = PromptGeneration(
        name='prompt generation 1', overhead=cfg_p.gen1_overhead.value)
    module_list = [
        remove_space,
        # summarize,
        generation1
    ]
    # run the modules on the prompt
    init_prompt.execute_modules(module_list)

    ask_prelimniary_er = CallOpenAI(
        prompt=init_prompt.get_prompt(), system_prompt=cfg_p.api_call_system.value)
    pre_er_model.set_model(ask_prelimniary_er())

    pre_er_model.display_model()

    print("second part")

    er_model = ErModel()
    second_prompt = Prompt()

    second_prompt.set_prompt(pre_er_model.get_model())
    generation2 = PromptGeneration(
        name='prompt generation 2', overhead=cfg_p.gen2_overhead.value)
    generation2(second_prompt)

    ask_json_array = CallOpenAI(prompt=second_prompt.get_prompt(
    ), system_prompt=cfg_p.api_call_system2, jsonResponse=True)
    er_model.set_model(ask_json_array())

    er_model.display_model()


if __name__ == "__main__":
    main()
