class Prompt:
    
    current_module = ''

    def __init__(self, prompt=''):
        self.prompt = prompt


    def get_current_module(self):
        print("the current module is: ", self.current_module)

    def get_current_prompt(self):
        if self.prompt == '' or self.prompt is None:
            print("The current prompt is empty!")
        print(self.prompt) 
