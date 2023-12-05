from enum import Enum
class config_prompt(Enum):
    gen1_overhead = 'Below is a Description of a datase read it carefully and give and your understanding if you want to make it an Entity relation model:'
    api_call_system = 'This is a description of an database act as a entity relation model guru.'
    gen2_overhead = """given er model return content of an array: [{
                    "__type": "Entity",
                    "_id": 1,
                    "_name": "store",
                },
                {
                    "__type": "Attribute",
                    "_id": 2,
                    "_name": "name",
                    "_parentId": 1,
                },"""
    api_call_system2 = """ put each element into dictionary then specify their type then the ids are incremental and if they belong to each other they have parent Id  """