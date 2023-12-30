class Process:
    def __init__(self,name):
        self.name = name


    def get_process_name(self):
        return self.name 

    def display_process_name(self):
        print("The process is: ",self.name)
