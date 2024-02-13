import json
import re


class ErModel():
    def __init__(self, model) -> None:
        self.model = model

    def set_model(self, model: str) -> None:
        self.model = model

    def get_model(self) -> str:
        return self.model

    def display_model(self) -> None:
        print(self.model)

    def transform_items_array_to_map(self, output_str):
        itemsMap = {}
        for item in output_str:
            item_id = item.get('_id')
            itemsMap[item_id] = item

        return itemsMap

    def process_model(self, output_format):
        # start off with no error message
        error_msg = ''
        delimiter = '###'
        # make the output format keys with a unique identifier
        new_output_format = {}
        for key in output_format.keys():
            new_output_format[f'{delimiter}{key}{delimiter}'] = output_format[key]

        res = self.model

        # try-catch block to ensure output format is adhered to
        try:
            # check key appears for each element in the output
            for key in new_output_format.keys():
                # if output field missing, raise an error
                if key not in res:
                    raise Exception(f"{key} not in json output")

            # if all is good, we then extract out the fields
            # Use regular expressions to extract keys and values
            pattern = fr",*\s*['|\"]{delimiter}([^#]*){delimiter}['|\"]: "

            matches = re.split(pattern, res[1:-1])

            # remove null matches
            my_matches = [match for match in matches if match != '']

            # remove the ' or " from the value matches
            curated_matches = [match[1:-1] if match[0]
                               in '\'"' else match for match in my_matches]

            # create a dictionary
            end_dict = {}
            for i in range(0, len(curated_matches), 2):
                end_dict[curated_matches[i]] = curated_matches[i+1]

            return end_dict

        except Exception as e:
            error_msg = f"\n\nResult: {res}\n\nError message: {str(e)}\nYou must use \"{delimiter}{{key}}{delimiter}\" to enclose the each {{key}}."
            print("An exception occurred:", str(e))
            print("Current invalid json format:", res)

        return {}

    def process_gp3_json_repsponse(self, output_format):
        coming_response = self.process_model(output_format)
        s1 = coming_response['itemsArray'].replace('\'', '\"')
        s2 = json.loads(s1)
        return s2

    def extract_and_convert_to_json(self, text=""):
        if text == "":
            text = self.model
        # Define a regular expression pattern to match the item array structure
        pattern = re.compile(r'"###itemsArray###":\s*(\[[^\]]*\])')

        # Search for the pattern in the text
        match = pattern.search(text)

        # Check if a match is found
        if match:
            # Extract and return the contents of the item array
            item_array_contents = match.group(1)
            s = json.loads(item_array_contents)
            return s  # Use eval to convert the string representation to a Python list
        else:
            # Return None if the pattern is not found
            return None

    def save_model(self, json_array_content, file_name="ER_model_final_response"):
        # load the place holder
        with open('json_placeholder.json', 'r') as jfile:
            place_holder = json.load(jfile)

        place_holder["erDesign"]["model"]["itemsArray"] = json_array_content
        result = self.transform_items_array_to_map(json_array_content)
        place_holder["erDesign"]["model"]["itemsMap"] = result

        with open(f'{file_name}.er', 'w') as new_file:
            json.dump(place_holder, new_file, indent=2)
