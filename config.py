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

    system_1_manual = "You are a database designer that produces entity relation model in following strict format:  *each entity :* entity entity_name  { comma sperated attributes (entity_type)} entity_type could be only [ id if its an identifier,optional if its existence is not necessary,multi if the entity can have multiple of the attribute ,nothing if it's not so specific] , *each relationship:* relationship relationship_name ( entity_name: relationship type, entity_name: relationship type){ attributes comma seperated } *relationship types are one of : [zero..many, one..many, one..one, many..many], *for each generalization do:* generalization entity_name <= {child entities_name}(type of generalization which could be one of the [(partial, exclusive),(partial), (overlapping,total), (exclusive,total), (overlapping), or empty] ) entities in generlatization part must be from entities part not new. If a section is empty do not put curly braces or parantenses just ignore it"

    delimiter = '###'

    code_lama_prompt_overhead = '''design entity-relationship model (ER model) restricted format between ``` ```:
entity <entity name> [ <attribute name> (id or null or multi or optional) ]
relationship <relationship name> {<entity name 1> : relationship type , <entity name 2> : relationship type } [<relationship attribute>]
generalization <entity name> [<entity name> (generalization type)] 

// generalization type = partial_exclusive or partial or overlapping_total or exclusive_total or overlapping or null
// only 2 entity can be in each relationship do not add more
// relationship type = zero_many or one_many or one_one or many_many or null
// the entity name in front of generalization is supertype and this list after is subtype

// do not add information from outside of the description
// be concise

given the above format with respect to comments follow explanation:
'''
    code_lama_34b_prompt_overhead = '''design entity-relationship model (ER model) restricted format between ``` ```:
entity <entity name> [ <attribute name> (id or null or multi or optional) , ]
relationship <relationship name> {<entity name 1> : relationship type , <entity name 2> : relationship type } [<relationship attribute> , ]
generalization <entity name> [<entity name> (generalization type) , ] 

// generalization type = partial_exclusive or partial or overlapping_total or exclusive_total or overlapping or null
// only 2 entity can be in each relationship do not add more
// relationship type = zero_many or one_many or one_one or many_many or null
// the entity name in front of generalization is supertype and this list after is subtype
// put , after each item in list 

// do not add information from outside of the description
// be concise

given the above format with respect to comments follow explanation:
'''
    mixtral_prompt_overhead = '''design entity-relationship model restricted format:
entity <entity name> [ <attribute name> (id or null or multi or optional) , ]
relationship <relationship name> {<entity name 1> : relationship type , <entity name 2> : relationship type } [<relationship attribute> , ]
generalization <entity name> [<entity name> (generalization type) , ] 

for example: 
entity hospital [ id (id) , address (optional) ]
entity doctor [ id (id) , name (null) ]
relationship has {hospital : zero_many , doctor : one_many } [ ]

// generalization type = partial_exclusive or partial or overlapping_total or exclusive_total or overlapping or null
// only 2 entity can be in each relationship do not add more
// relationship type = zero_many or one_many or one_one or many_many or null
// the entity name in front of generalization is supertype and this list after is subtype
// put , after each item in list 
// carefull paranthesis and other symbols where to place them 


// do not add information from outside of the description
// be concise

given the above format with respect to comments follow explanation:
'''


class config_model(Enum):
    code_llama_70b = 'codellama/codellama-70b-instruct'
    code_llama_34b = 'meta-llama/codellama-34b-instruct'
    gpt_4 = 'openai/gpt-4'
    toppy = 'undi95/toppy-m-7b'
    open_chat_7b = 'openchat/openchat-7b'
    zephyr = 'huggingfaceh4/zephyr-7b-beta'
    mythomax = 'gryphe/mythomax-l2-13b'
    mixtral = 'mistralai/mixtral-8x7b-instruct'
    mistral = 'mistralai/mistral-medium'
    claude_2 = 'anthropic/claude-2'
    xwin = 'xwin-lm/xwin-lm-70b'
    synthia = 'migtissera/synthia-70b'
    openhermes = 'teknium/openhermes-2.5-mistral-7b'
    nous_hermes_2_mixtral = 'nousresearch/nous-hermes-2-mixtral-8x7b-dpo'
    gemini = 'google/gemini-pro'
