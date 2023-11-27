from dotenv import load_dotenv
import os

from src.input import get_input
from src.pre_processing_module import input_cleaner

load_dotenv()
api_key = os.getenv("API_KEY")

def main():
    print("Welcome to Designer-ai-1 !!!")
    # print("here is the api key=>",api_key)
    input = get_input()
    input = input_cleaner(input)
    print("================================================================")
    print("================================================================")
    print("================================================================")
    print(input)

if __name__ == "__main__":
    main()