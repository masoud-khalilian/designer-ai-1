from enum import Enum


class config_prompt(Enum):
    user_1 = 'give me Entity relation model:'
    system_1 = '/* Entities */ for each detected entity do : \nentity name of entity* { name of attributes of the entity seperated with \n} \n\n , /* Relationships */ for each relationship do: \nrelationship (name of the relationship) ( entity1: relationship type, entity2: relationship type){ name of the attributes of the relationship seperated by \n} *relationship types are one of : zero...many, one...many, one...one, many...many * \n\n  /* Generalizations */ \nParententity <= {\n name of the child entities}(type of generalization)'

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
