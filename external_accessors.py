'''
Placeholder class for external accessors,
this is to tell us the teacher is treated as a seperate entity 
from the base algorithm
'''
class Teacher:
    def __init__(self, test_param):
        self.test_param = test_param

    def membership_query(self):
        print("Hello World")

# This is a test for the code
teacher = Teacher("test")
teacher.membership_query()