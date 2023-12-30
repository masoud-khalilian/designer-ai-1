from enum import Enum


class config_prompt(Enum):
    gen1_overhead = 'Below is a Description of a datase read it carefully and give and your understanding if you want to make it an Entity relation model:'
    api_call_system = 'This is a description of an database act as a entity relation model guru.'
    gen2_overhead = """create a valid JSON array of objects for given er model following this format:
                [{
                    "__type": "Entity",
                    "_id": 1,
                    "_name": "store",
                },
                {
                    "__type": "Attribute",
                    "_id": 2,
                    "_name": "name",
                    "_parentId": 1,
                },
                """
    api_call_system2 = """ return as a json given the ER model"""
    sample_item_array_strict_format = {

        "itemsArray": [
            {
                "__type": "Entity",
                "_id": "number id wich must be unique between all element of itemsArray",
                "_name": "name of the entity",
                "_x": "an number -400 to 400",
                "_y": "an number -400 to 400",
                "_mag": "boolean false"

            },
            {
                "__type": "Attribute",
                "_id": "number id wich must be unique between all element of itemsArray",
                "_name": "name of the attribute",
                "_parentId": "a number indicate the id of which entity this atribute refering to",
                "_identifier": "boolean true or false only for atrribute type",
                "_x": "a number -400 to 400",
                "_y": "a number -400 to 400",
                "_externalIdentifier": "boolean true or false only for atrribute type",
                "_cardinality": 'chose one from the list ["1_1", "1_N", "0_N","0_1","_"]',
            },
            {
                "__type": "Relationship",
                "_id": "number id wich must be unique between all element of itemsArray",
                "_name": "name of relationship",
                "_x": "an number -400 to 400",
                "_y": "an number -400 to 400"
            },
            {
                "__type": "Participation",
                "_id": "number id wich must be unique between all element of itemsArray",
                "_entityId": "number id of entity which gets connected to relationship",
                "_relationshipId": "number id of relationship",
                "_x": "an number -400 to 400",
                "_y": "an number -400 to 400",
                "_tableId": "return null",
                "_cardinality": 'chose one from the list ["1_1", "1_N", "0_N","0_1","_"]',
                "_externalIdentifier": "boolean true or false only for atrribute type",
                "_role": ""
            },
            {
                "__type": "Participation",
                "_id": "number id wich must be unique between all element of itemsArray",
                "_entityId": "number id of entity which gets connected to relationship",
                "_relationshipId": "number id of relationship",
                "_x": "an number -400 to 400",
                "_y": "an number -400 to 400",
                "_tableId": "return null",
                "_cardinality": 'chose one from the list ["1_1", "1_N", "0_N","0_1","_"]',
                "_externalIdentifier": "boolean true or false only for atrribute type",
                "_role": ""
            }]}
