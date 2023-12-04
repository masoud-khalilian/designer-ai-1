class ErModel():
    def __init__(self) -> None:
        self.model = ''

    def set_model(self,model:str)->None: 
        self.model = model

    def get_model(self)->str:
        return self.model
    
    def display_model(self)->None:
        print(self.model)    