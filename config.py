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
                "_x": "a random number  from -400 to 400",
                "_y": "a random number from -400 to 400",
                "_mag": "boolean False"

            },
            {
                "__type": "Attribute",
                "_id": "number id which must be unique between all element of itemsArray",
                "_name": "name of the attribute",
                "_parentId": "a number indicates the id of the entity which this atribute refering to",
                "_identifier": "boolean True or False only for atrribute type",
                "_x": "a random number between -5 to 5 of the parent entity",
                "_y": "a random number between -5 to 5 of the parent entity",
                "_externalIdentifier": "boolean True or False only for atrribute type",
                "_cardinality": 'chose one from the list ["1_1", "1_N", "0_N","0_1","_"]',
            },
            {
                "__type": "Relationship",
                "_id": "number id which must be unique between all element of itemsArray",
                "_name": "name of relationship",
                "_x": "a number between both related entities' '_x' ",
                "_y": "a number between both related entities' '_y' "
            },
            {
                "__type": "Participation",
                "_id": "number id which must be unique between all element of itemsArray",
                "_entityId": "number id of entity which gets connected to relationship",
                "_relationshipId": "number id of relationship",
                "_tableId": "return null",
                "_cardinality": 'chose one from the list ["1_1", "1_N", "0_N","0_1","_"]',
                "_externalIdentifier": "boolean True or False only for atrribute type",
                "_role": ""
            },
            {
                "__type": "Generalization",
                "_id": "number id which must be unique between all element of itemsArray",
                "_type": "shows the type of generalization, (example: a flight ticket's generalization type is 'class' which refers to the ticket's 'first_class', 'business_class' and 'economy_class'.)",
                "_entityId": "the id corresponding to the parent of the generalization. (in case of flight ticket should return the '_id' of 'ticket' entity)"
            },
            {
                "__type": "GeneralizationChild",
                "_id": "number id which must be unique between all element of itemsArray",
                "_entityId": "indicates the '_id' of child entity (in case of flight tickets, it would be the id of 'business_class' or 'first_class' or 'economy class')",
                "_generalizationId": "refers to the '_id' of the 'Generalization'"
            }
        ]}

    delimiter = '###'
