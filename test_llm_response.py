import json
from src.er_model import ErModel
from src.array_generator import ArrayGenerator
# from custom_array_generator import CustomArrayGenerator

# this function will run the program with pre maide response from the server
# it basically starts from second part of the programm
# the pre made er respnse is saved at test_sample_llm_response.txt


def main():

    file_path = 'test_sample_llm_response.txt'
    output_file_name = "er_model"

    with open(file_path, 'r') as file:
        saved_respose = file.read()

    pre_er_model = ErModel(saved_respose)
    er3 = pre_er_model.get_model()
    er_model = ErModel(er3)
    generator = ArrayGenerator(er3)
    json_array = generator.get_transformed_array()

    python_list = json_array.tolist()
    json_string = json.dumps(python_list)
    res = json.loads(json_string)
    res = list(filter(lambda x: x is not None, res))
    er_model.save_model(res, file_name=output_file_name)

    print(f"JOB SUCCESSFULLY DONE !!!\n")


if __name__ == "__main__":
    main()
