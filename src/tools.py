import os
from datetime import datetime


def process_json(output_str):
    itemsMap = {}
    for item in output_str:
        item_id = item.get('_id')
        itemsMap[item_id] = item
    return itemsMap


def log_preliminary_er(input_string: str, input_tag: str):
    file_path = "preliminary_er_log.txt"

    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create or open the file in append mode
    with open(file_path, 'a') as file:
        # If the file doesn't exist, add a header
        if os.path.isfile(file_path):
            file.write("ID,Time,Tag,Text\n")
            row_id = sum(1 for line in open(file_path))
        else:
            # If the file doesn't exist, create it and add the header
            file.write("ID,Time,Tag,Text\n")
            row_id = 1

        # Write the new row to the file
        file.write(f"{row_id},{current_time},{input_tag},{input_string}\n")

    print(f"Data saved to {file_path} with ID {row_id}")
