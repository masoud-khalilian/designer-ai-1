from src.er_model import ErModel
from src.api_module import CallOpenAI
from src.prompt import Prompt
from src.pre_processing_module import RemoveSpace,Summarize,PropmtGeneration


def main():
    print("Welcome to Designer-ai-1 !!!")
    prompt = Prompt()
    er_model = ErModel()
    prompt.get_input()
    prompt.display_current_prompt()

    remove_space = RemoveSpace() 
    summarize = Summarize()
    generation1 = PropmtGeneration()
    module_list = [
        remove_space,
        # summarize,
        generation1
        ]
    prompt.execute_modules(module_list)
    prompt.display_current_prompt()

    call_openai = CallOpenAI(overhead=prompt.get_prompt())
    call_openai(er_model)

    er_model.display_model()

if __name__ == "__main__":
    main()