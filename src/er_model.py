class ErModel():
    def __init__(self) -> None:
        self.model = ''

    def set_model(self,model:str)->None: 
        self.model = model

    def get_model(self)->str:
        return self.model
    
    def display_model(self)->None:
        print(self.model)

    def transform_items_array_to_map(itemsArray):
        itemsMap = {}

        for item in itemsArray:
            item_id = item["_id"]
            itemsMap[item_id] = item

        return itemsMap