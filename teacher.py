from constants import _Const
from dfa import DFA
CONST = _Const()

'''
this is to tell us the teacher is treated as a seperate entity 
from the base algorithm, defines base actions of teacher
'''
class Teacher:

    def membership_query(self, test_word):
        return CONST.POS
    
    def equivalence_query(self, proposed_dfa: DFA):
        counter_example = None
        return True, counter_example

if __name__ == "__main__":
    teacher = Teacher()
    print(teacher.membership_query("test"))