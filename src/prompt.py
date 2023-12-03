class Prompt:
    
    current_module = ''

    def __init__(self, prompt=''):
        self.prompt = prompt

    def get_prompt(self):
        return self.prompt
    
    def set_prompt(self,p):
        self.prompt = p

    def get_input(self):
        print("Enter the prompt don't worry we will give you the ER model: \nPress Enter twice to finish.")
    
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            lines.append(line)
        
        # Join the lines to form the complete text
        text = '\n'.join(lines)

        self.prompt = text
    
    def get_current_module(self):
        print("the current module is: ", self.current_module)

    def display_current_prompt(self):
        if self.prompt == '' or self.prompt is None:
            print("The current prompt is empty!")
        print(self.prompt) 

    def execute_modules(self, modules):
        for module in modules:
            module(self)
            print("module ",module.name,' has been executed.')
            self.current_module = module.name