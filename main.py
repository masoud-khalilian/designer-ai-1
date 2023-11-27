from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

def main():
    print("Welcome to Designer-ai-1 !!!")
    print("here is the api key=>",api_key)

if __name__ == "__main__":
    main()