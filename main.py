from dotenv import load_dotenv
import os

from src.prompt import Prompt
from src.input import get_input
from src.pre_processing_module import input_cleaner

load_dotenv()
api_key = os.getenv("API_KEY")

def main():
    print("Welcome to Designer-ai-1 !!!")
    prompt = Prompt()
    prompt.get_current_prompt()

if __name__ == "__main__":
    main()