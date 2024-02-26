'''
This is the standard entry point for the project, 
we'll be adding:
1. Ability to choose algorithms
2. Ability to choose teacher interaction (if scope)
'''

#This is a placeholder class for now, needs to be filled in
class LNL_Interface:
    def __init__(self, test_param):
        self.test_param = test_param

    def start(self):
        print("Hello World")

# This is where the actual run starts
interface = LNL_Interface("test")
interface.start()