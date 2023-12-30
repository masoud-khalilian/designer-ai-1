from enum import Enum


class config_prompt(Enum):
    user_1 = 'give me Entity relation model:'
    system_1 = '1-name of the Entity next line the attributes if primary key put infront of them (PK) next line the name of relationship and what sort of relationships is then start from the next entity like 2-entity2'

    api_call_system2 = "Return according to this example with 1-make sure all id must be incremental "
    strict_format = {
        "itemsArray": [
            {
                "__type": "Entity",
                "_id": "number id which must be unique between all element of itemsArray",
                "_name": "name of the entity",
                "_x": "an number -400 to 400",
                "_y": "an number -400 to 400",
                "_mag": "boolean false"

            },
            {
                "__type": "Attribute",
                "_id": "number id which must be unique between all element of itemsArray",
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
                "_id": "number id which must be unique between all element of itemsArray",
                "_name": "name of relationship",
                "_x": "an number -400 to 400",
                "_y": "an number -400 to 400"
            },
            {
                "__type": "Participation",
                "_id": "number id which must be unique between all element of itemsArray",
                "_entityId": "number id of entity which gets connected to relationship",
                "_relationshipId": "number id of relationship",
                "_x": "an number -400 to 400",
                "_y": "an number -400 to 400",
                "_tableId": "return null",
                "_cardinality": 'chose one from the list ["1_1", "1_N", "0_N","0_1","_"]',
                "_externalIdentifier": "boolean true or false only for atrribute type",
                "_role": ""
            }]}

    delimiter = '###'
