from dotenv import load_dotenv
import os

from src.prompt import Prompt
from src.pre_processing_module import RemoveSpace,Summarize,PropmtGeneration

load_dotenv()
api_key = os.getenv("API_KEY")

def main():
    print("Welcome to Designer-ai-1 !!!")
    prompt = Prompt()
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


if __name__ == "__main__":
    main()