import json
import re
import random
import numpy as np

from src.er_model import ErModel

# from er_model import ErModel


def find_entity_id(name, data):
    for item in data:
        if "__type" in item and item["__type"] == "Entity" and "_name" in item and item["_name"] == name:
            return item["_id"]
    return None


def find_relation_id(name, data):
    for item in data:
        if "__type" in item and item["__type"] == "Relationship" and "_name" in item and item["_name"] == name:
            return item["_id"]
    return None


def map_to_enum_format(value):
    if value == "one..one" or value == "one_one":
        return "1_1"
    elif value == "zero..one" or value == "zero_one":
        return "0_1"
    elif value == "zero..zero" or value == "zero_zero":
        return "0_0"
    elif value == "one..many" or value == "one_many":
        return "1_N"
    elif value == "many..many" or value == "many_many":
        return "N_N"
    elif value == "zero..many" or value == "zero_many":
        return "0_N"
    # Add more cases as needed
    else:
        return "_"


def map_general_type(value):
    if value == "partial, exclusive" or "partial_exclusive":
        return "p_e"
    elif value == "partial, overlapping" or "overlapping":
        return "p_o"
    elif value == "total, exclusive" or "exclusive_total":
        return "t_e"
    elif value == "total, overlapping" or "overlapping_total":
        return "t_o"
    # Add more cases as needed
    else:
        return "p_e"


def extract_name_relations(text):

    parts = text.split(':')
    if len(parts) == 2:
        name = parts[0].strip()
        value = parts[1].strip()
        parts = value.split('external')
        is_e = False
        value = map_to_enum_format(value)

        if len(parts) > 1:
            value = "1_1"
            is_e = True

        return name, value, is_e
    else:
        # Return None if the text doesn't match the expected format
        return None


def is_primary_attribute(input_string):
    modified_string = re.sub(r"\(id\)", "", input_string)
    has_id = modified_string != input_string
    return modified_string.strip(), has_id


def is_external_attribute(input_string):
    modified_string = re.sub(r"\(external\)", "", input_string)
    has_id = modified_string != input_string
    return modified_string.strip(), has_id


def get_attribute_cardinality(input_string):
    # Define the pattern using regular expressions
    pattern = r'(\w+)\s*(?:\(([^)]*)\))?'

    # Use re.match to find the pattern in the input text
    match = re.match(pattern, input_string)

    # Check if a match is found
    if match:
        # Extract the values from the matched groups
        keyword = match.group(1).strip()
        cardinality = match.group(2)

        # Map cardinality to the specified format
        cardinality_mapping = {
            'multi': '1_N',
            'optional': '0_1',
            '(optional, multi)': '0_N',
            None: '1_1'
        }

        # Convert cardinality to the specified format
        cardinality = cardinality_mapping.get(cardinality, '1_1')

        return keyword, cardinality
    else:
        # Return None if no match is found
        return keyword, '1_1'


def process_tuple_entities(input_tuple, current_position):
    global last_element_id_global
    result_list = np.array([])
    key, attributes = input_tuple
    entity_id = last_element_id_global
    entity_dict = {
        "__type": "Entity",
        "_id": entity_id,
        "_name": key,
        "_x": current_position[0],
        "_y": current_position[1],
        "_mag": False
    }
    result_list = np.append(result_list, entity_dict)
    attribute_list = attributes.split(', ')
    attribute_dicts = []
    for attribute in attribute_list:
        last_element_id_global = last_element_id_global+1
        name, is_p = is_primary_attribute(attribute)
        name, is_e = is_external_attribute(name)
        name, cardinality = get_attribute_cardinality(name)
        att_dic = {
            "__type": "Attribute",
            "_id": last_element_id_global,
            "_name": name,
            "_identifier": is_p,
            "_externalIdentifier": is_e,
            "_parentId": entity_id,
            "_cardinality": cardinality,
            "_x": random.randint(-210, 210),
            "_y": random.choice([-120, 0, 120, 180, -180])

        }
        attribute_dicts = np.append(attribute_dicts, att_dic)
    result_list = np.append(result_list, attribute_dicts)
    return result_list


def process_tuple_relations(input_tuple, enity_data):
    global last_element_id_global
    result_list = np.array([])
    key, attributes = input_tuple
    entity_id = last_element_id_global
    attribute_list = attributes.split(', ')
    attribute_dicts = []
    x = [0 for i in range(100)]
    y = [0 for i in range(100)]
    for attribute in attribute_list:
        last_element_id_global = last_element_id_global + 1
        name, rel_type, is_external = extract_name_relations(attribute)
        parent_id = find_entity_id(name, data=enity_data)
        for i in enity_data:
            if i["_id"] == parent_id:
                x[entity_id] += i["_x"]
                y[entity_id] += i["_y"]

        att_dic = {
            "__type": "Participation",
            "_id": last_element_id_global,
            "_entityId": parent_id,
            "_relationshipId": entity_id,
            "_tableId": None,
            "_cardinality": rel_type,
            "_externalIdentifier": is_external,
            "_role": ""
        },
        entity_dict = {
            "__type": "Relationship",
            "_id": entity_id,
            "_name": key,
            "_x": x[entity_id]/2,
            "_y": y[entity_id]/2
        },
        result_list = np.append(result_list, entity_dict)
        attribute_dicts = np.append(attribute_dicts, att_dic)
    result_list = np.append(result_list, attribute_dicts)
    return result_list


def extract_entities(input_string):
    global last_element_id_global
    entity_pattern = r'entity\s+(\w+)\s+\[\s*(.*?)\s*\]'
    matches = re.findall(entity_pattern, input_string)
    entity_data = matches
    # for match in matches:
    #     entity_name = match[0].strip()
    #     brace_content = match[2].strip() if match[2] else None
    #     entity_data.append((entity_name, brace_content))

    current_position = [0, 0]
    obj_entity_list = np.array([])
    number = 2
    for enity in enumerate(entity_data):
        direction = number % 2
        current_position = [
            current_position[0] + (500 * (1-direction)), current_position[1] + (500 * direction)]
        number += 1
        if enity[1][1] is not None:
            j = process_tuple_entities(enity[1], current_position)
            last_element_id_global = last_element_id_global+1
            obj_entity_list = np.append(obj_entity_list, j)
        else:
            last_element_id_global = last_element_id_global+1
            obj_entity_list = np.append(obj_entity_list, [{
                "__type": "Entity",
                "_id": last_element_id_global,
                "_name": enity[1][0],
                "_x": current_position[0],
                "_y": current_position[1],
                "_mag": False
            }])
    return obj_entity_list


def extract_relations(input_string, e_data):
    global last_element_id_global
    pattern = r'\brelationship\s+(\w+)\s*\{([^}]*)\}'
    matches = re.findall(pattern, input_string)
    relation_data = []

    for match in matches:
        relation_name = match[0]
        entity_cardinalities = match[1].strip()
        relation_data.append((relation_name, entity_cardinalities))

    obj_entity_list = np.array([])
    for rels in enumerate(relation_data):
        j = process_tuple_relations(rels[1], e_data)
        last_element_id_global = last_element_id_global+1
        obj_entity_list = np.append(obj_entity_list, j)

    return obj_entity_list


def extract_relation_attribute(input_string, e_data):
    global last_element_id_global

    # Define the pattern using regular expressions
    pattern = r'relationship\s+([^\(]+)\s*\(\s*([^)]*)\s*\)\s*\{\s*([^}]*)\s*\}'

    # Use re.search to find the pattern in the input_text
    match = re.search(pattern, input_string)

    # Check if a match is found
    if match:
        # Extract the values from the matched groups
        connection_name = match.group(1).strip()
        args = match.group(2).strip()
        brace_content = match.group(3).strip()

        # Split the args by commas and create tuples
        args_items = [item.strip() for item in brace_content.split(',')]

        # Create a list of tuples with connection names and brace items
        relation_atribute_tuple = [(connection_name, item)
                                   for item in args_items]
        result = []
        for attribute in relation_atribute_tuple:

            last_element_id_global = last_element_id_global + 1
            dic = {
                "__type": "Attribute",
                "_id": last_element_id_global,
                "_name": attribute[1],
                "_identifier": False,
                "_externalIdentifier": False,
                "_cardinality": "1_1",
                "_parentId": find_relation_id(attribute[0], data=e_data),
                "_x": random.randint(-210, 210),
                "_y": random.choice([-120, 0, 120, 180, -180])
            }

            result.append(dic)
        return result


def extract_gerneralization(input_string, e_data):
    global last_element_id_global
    # pattern = r'(\w+)\s*<=\s*{\s*([^}]*)\s*}\s*\(([^)]*)\)'
    # matches = re.finditer(pattern, input_string)
    # pattern = r'generalization\s+([\w\s]+)\s*\[([^]]+)\]'
    pattern = r'\bgeneralization\s+(\w+)\s*\[([^]]*)\]'
    matches = re.findall(pattern, input_string)
    results = []

    for match in matches:
        parent_entity = match[0]
        entities = [entity.strip() for entity in match[1].split(',')]
        first_entity = entities[0]
        first_entity_type = re.search(r'\((.*?)\)', first_entity)
        result = {
            "parent_entity": parent_entity,
            "entities": entities,
            "type": first_entity_type
        }
        last_element_id_global = last_element_id_global + 1
        general_id = last_element_id_global
        general_type = map_general_type(result["type"])
        general_head = {
            "__type": "Generalization",
            "_id": general_id,
            "_type": general_type,
            "_entityId": find_entity_id(result["parent_entity"], e_data),
        }
        general_childs = []
        for g_child in result["entities"]:
            g_child = g_child.split(" ")[0]
            # find the child if does not exist pass
            c_entity = find_entity_id(g_child, e_data)
            if c_entity == None:
                continue
            last_element_id_global = last_element_id_global + 1
            child = {
                "__type": "GeneralizationChild",
                "_id": last_element_id_global,
                "_entityId": find_entity_id(g_child, e_data),
                "_generalizationId": general_id
            }
            general_childs.append(child)

        results.extend(general_childs)
        results.insert(0, general_head)

    return results if results else None


class CustomArrayGenerator():
    global last_element_id_global
    last_element_id_global = 1

    def __init__(self, er_code: str) -> None:
        self.er_code = er_code
        self.obj_list = []

    def transform_er_code(self):
        array_json = np.array([])
        er_code = self.er_code
        er_code = re.findall(r'```(.*?)```', er_code, re.DOTALL)
        if len(er_code) > 1:
            er_code = er_code[0]
        else:
            er_code = self.er_code

        er_code = er_code.replace("\n", " ")
        er_code = re.sub(r'\s+', ' ', er_code)
        er_code = re.sub(r'/\*.*?\*/', '', er_code, flags=re.DOTALL)
        entities_attributes = extract_entities(er_code)
        array_json = np.append(array_json, entities_attributes)

        rels = extract_relations(er_code, entities_attributes)
        array_json = np.append(array_json, rels)

        gerneralization = extract_gerneralization(er_code, array_json)
        array_json = np.append(array_json, gerneralization)

        relation_attribute = extract_relation_attribute(er_code, array_json)
        array_json = np.append(array_json, relation_attribute)

        return array_json, er_code

    def display(self):
        global last_element_id_global
        last_element_id_global = 1
        arr, cleanjson = self.transform_er_code()
        print(cleanjson)

    def get_transformed_array(self):
        global last_element_id_global
        last_element_id_global = 1
        array_json, cleanjson = self.transform_er_code()
        return array_json


# er3 = """
# Here is the ER model for the bookstore database:

# ```
# entity Bookstore [id (id), address (null)]
# entity Book [isbn (id), name (null)]
# relationship sells {Bookstore : zero_many, Book : one_many}
# ```

# Explanation:

# *   The `Bookstore` entity has two attributes: `id` (primary key) and `address`.
# *   The `Book` entity has two attributes: `isbn` (primary key) and `name`.
# *   The `Sells` relationship connects `Bookstore` and `Book` entities. A bookstore can sell many books, and a book can be sold by many bookstores.
# """

# er3 = """```
# entity Person [
#     id (id),
#     name (null),
#     surname (null),
#     telephone (null),
#     email (null),
#     facebook (null)
# ]
# entity Book [
#     isbn (id),
#     title (null),
#     co-authors (multi)
# ]
# entity Chapter [
#     title (null)
# ]
# entity Author [
#     id (id),
#     name (null),
#     surname (null),
#     pseudonym (null)
# ]
# entity Consultation [
#     person (id),
#     date (null),
#     book (id),
#     state_of_wear (null)
# ]
# relationship Consultation {
#     Person : one_many,
#     Book : one_many
# }
# relationship Authorship {
#     Book : one_many,
#     Author : one_many
# }
# relationship Chapter {
#     Book : one_many,
#     Chapter : many_many
# }
# generalization Book [
#     Book (partial_exclusive),
#     Series (partial)
# ]
# ```

# Explanation:

# *   **Person** entity: represents the person who registers at the museum and acquires a card. It has attributes such as id, name, surname, telephone, email, and facebook.
# *   **Book** entity: represents the books available at the museum. It has attributes such as isbn, title, and co-authors.
# *   **Chapter** entity: represents the titles of the chapters of the book.
# *   **Author** entity: represents the authors of the book. It has attributes such as id, name, surname, and pseudonym.
# *   **Consultation** entity: represents the consultation of a book by a person. It has attributes such as person, date, book, and state_of_wear.
# *   **Consultation** relationship: represents the relationship between Person and Book entities. A person can consult many books, and a book can be consulted by many people.
# *   **Authorship** relationship: represents the relationship between Book and Author entities. A book can have many authors, and an author can write many books.
# *   **Chapter** relationship: represents the relationship between Book and Chapter entities. A book can have many chapters, and a chapter can belong to many books.
# *   **Book** generalization: represents the generalization of Book entity into Series entity. A book can be part of a series, and a series can have many books.
# """

# er3 = """  ```
# entity bookstore [
#     id (id),
#     address (multi)
# ]
# entity book [
#     isbn (id),
#     name (multi)
# ]
# relationship sell [
#     bookstore (one_many),
#     book (many_many)
# ]
# ```

# The ERM follows the format:

# *   Entity bookstore:
#     *   id (id): unique identifier for each bookstore
#     *   address (multi): multiple addresses for each bookstore
# *   Entity book:
#     *   isbn (id): unique identifier for each book
#     *   name (multi): multiple names for each book
# *   Relationship sell:
#     *   bookstore (one_many): each bookstore can sell many books
#     *   book (many_many): each book can be sold by many bookstores

# This ERM design meets the requirements:

# *   Each bookstore has a unique id and address.
# *   Each book has a unique isbn and name.
# *   Each book can be sold by many bookstores. "
# """

# er_model = ErModel(er3)
# generator = ArrayGenerator(er3)
# json_array = generator.get_transformed_array()
# print(json_array)

# python_list = json_array.tolist()
# json_string = json.dumps(python_list)
# res = json.loads(json_string)
# res = list(filter(lambda x: x is not None, res))
# er_model.save_model(res, file_name=f"er_model_manual")
