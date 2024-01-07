import json
import re
import random
import numpy as np

from er_model import ErModel


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
    if value == "one..one":
        return "1_1"
    elif value == "zero..one":
        return "0_1"
    elif value == "zero..zero":
        return "0_0"
    elif value == "one..many":
        return "1_N"
    elif value == "many..many":
        return "N_N"
    elif value == "zero..many":
        return "0_N"
    # Add more cases as needed
    else:
        return "_"


def map_general_type(value):
    if value == "partial, exclusive":
        return "p_e"
    elif value == "partial, overlapping":
        return "p_o"
    elif value == "total, exclusive":
        return "t_e"
    elif value == "total, overlapping":
        return "t_o"
    # Add more cases as needed
    else:
        return "_"


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


def process_tuple_entities(input_tuple):
    global last_element_id_global
    print(type(input_tuple))
    print(input_tuple)

    result_list = np.array([])
    key, attributes = input_tuple
    entity_id = last_element_id_global
    entity_dict = {
        "__type": "Entity",
        "_id": entity_id,
        "_name": key,
        "_x": random.randint(-700, 700),
        "_y": random.randint(-700, 700),
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
            "_x": random.randint(-700, 700),
            "_y": random.randint(-700, 700)
        }

        attribute_dicts = np.append(attribute_dicts, att_dic)
    result_list = np.append(result_list, attribute_dicts)
    return result_list


def process_tuple_relations(input_tuple, enity_data):
    global last_element_id_global
    result_list = np.array([])
    key, attributes = input_tuple
    entity_id = last_element_id_global
    entity_dict = {
        "__type": "Relationship",
        "_id": entity_id,
        "_name": key,
        "_x": random.randint(-700, 700),
        "_y": random.randint(-700, 700)
    },
    result_list = np.append(result_list, entity_dict)
    attribute_list = attributes.split(', ')
    attribute_dicts = []
    for attribute in attribute_list:
        last_element_id_global = last_element_id_global+1
        name, rel_type, is_external = extract_name_relations(attribute)
        parent_id = find_entity_id(name, data=enity_data)
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

        attribute_dicts = np.append(attribute_dicts, att_dic)
    result_list = np.append(result_list, attribute_dicts)
    return result_list


def extract_entities(input_string):
    global last_element_id_global
    pattern = r'\bentity\s+(\w+)\s*({([^}]*)})?'
    matches = re.findall(pattern, input_string)

    entity_data = []

    for match in matches:
        entity_name = match[0].strip()
        brace_content = match[2].strip() if match[2] else None
        entity_data.append((entity_name, brace_content))

        # word = match[0]
        # curly_braces_structure = match[1].strip()
        # print((word, curly_braces_structure))
        # entity_data.append((word, curly_braces_structure))
    print(entity_data)
    obj_entity_list = np.array([])
    for enity in enumerate(entity_data):
        print(enity)
        if enity[1][1] is not None:
            j = process_tuple_entities(enity[1])
            last_element_id_global = last_element_id_global+1
            obj_entity_list = np.append(obj_entity_list, j)
        else:
            last_element_id_global = last_element_id_global+1
            obj_entity_list = np.append(obj_entity_list, [{
                "__type": "Entity",
                "_id": last_element_id_global,
                "_name": enity[1][0],
                "_x": random.randint(-700, 700),
                "_y": random.randint(-700, 700),
                "_mag": False
            }])
    return obj_entity_list


def extract_relations(input_string, e_data):
    global last_element_id_global
    pattern = r'\brelationship\s+(\w+)\s*\(([^)]*)\)'
    matches = re.findall(pattern, input_string)

    relation_data = []

    for match in matches:
        word = match[0]
        curly_braces_structure = match[1].strip()
        relation_data.append((word, curly_braces_structure))

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
                "_x": random.randint(-700, 700),
                "_y": random.randint(-700, 700)
            }
            result.append(dic)
        return result


def extract_gerneralization(input_string, e_data):
    global last_element_id_global
    pattern = r'(\w+)\s*<=\s*{\s*([^}]*)\s*}\s*\(([^)]*)\)'
    matches = re.finditer(pattern, input_string)

    results = []

    for match in matches:
        parent_entity = match.group(1)
        entities = [entity.strip() for entity in match.group(2).split(',')]
        entity_type = match.group(3)
        result = {
            "parent_entity": parent_entity,
            "entities": entities,
            "type": entity_type
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


class ArrayGenerator():
    global last_element_id_global
    last_element_id_global = 1

    def __init__(self, er_code: str) -> None:
        self.er_code = er_code
        self.obj_list = []

    def transform_er_code(self):
        array_json = np.array([])
        er_code = self.er_code
        er_code = er_code.replace("\n", " ")
        er_code = re.sub(r'\s+', ' ', er_code)
        er_code = re.sub(r'/\*.*?\*/', '', er_code, flags=re.DOTALL)
        print("\n")
        print(er_code)
        print("\n")
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


# er3 = '/* Entities */\nentity BOOK {\n    ISBN (id),\n    Name\n}\nentity BOOK_STORE {\n    Id (id),\n    Address\n}\n\n/* Relationships */\nrelationship HAS (\n    BOOK: one..one,\n    BOOK_STORE: one..many\n)'
# er3 = "/* Entities */\nentity USER {\n    UCode (id),\n    Nickname,\n    Email,\n    Facebook_page (optional)\n}\nentity SUPPORTER {\n    Sponsorship_fee\n}\nentity MULTIMEDIA_CONTENT {\n    MCCode (external),\n    Name,\n    Description,\n    Keywords (multi)\n}\nentity AUDIO {\n    Duration\n}\nentity PICTURE {\n    Format\n}\nentity VIDEO {\n    Duration,\n    Resolution\n}\nentity TIME {\n    Date (id)\n}\n\n/* Relationships */\nrelationship PROVIDE (\n    USER: zero..many,\n    MULTIMEDIA_CONTENT: one..one external\n)\nrelationship CONNECT (\n    USER: zero..many,\n    TIME: one..many\n) {\n    Minutes\n}\n\n/* Generalizations */\nUSER <= {\n    SUPPORTER\n} (partial, exclusive)\nMULTIMEDIA_CONTENT <= {\n    AUDIO,\n    PICTURE,\n    VIDEO\n} (total, exclusive)"
er3 = "/* Entities */\nentity CUSTOMER {\n    TaxCode (id),\n    CName,\n    CAddress,\n    email (optional)\n}\nentity PRIVATE\nentity COMPANY {\n    Vat,\n    PhoneNum (multi)\n}\nentity FORNITURE_MODEL {\n    MCode (id),\n    Size {\n        Height,\n        Width,\n        Depth\n    }\n}\nentity SUPPLIER {\n    VatNum (id),\n    SName,\n    PhoneNum\n}\nentity SALE_CONTRACT {\n    SCCode (id),\n    Date,\n    TotalPrice\n}\nentity VAN {\n    PlateNum (id),\n    Model,\n    RegistrationYear\n}\n\n/* Relationships */\nrelationship SUPPLIED_BY (\n    FORNITURE_MODEL: one..one,\n    SUPPLIER: zero..many\n)\nrelationship SIGNED_BY (\n    CUSTOMER: zero..many,\n    SALE_CONTRACT: one..one\n)\nrelationship INCLUDED_MODELS (\n    FORNITURE_MODEL: zero..many,\n    SALE_CONTRACT: one..many\n)\nrelationship DELIVERY (\n    SALE_CONTRACT: one..one,\n    VAN: one..one\n) {\n    DeliveryDate,\n    DeliveryTime\n}\n\n/* Generalizations */\nCUSTOMER <= {\n    PRIVATE,\n    COMPANY\n} (total, exclusive)"

er_model = ErModel(er3)
generator = ArrayGenerator(er3)
json_array = generator.get_transformed_array()

python_list = json_array.tolist()
json_string = json.dumps(python_list)
res = json.loads(json_string)
er_model.save_model(res, file_name=f"er_model_manual")
