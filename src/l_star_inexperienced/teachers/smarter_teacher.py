from .teacher import Teacher
from ..common.constants import _Const
from ..dfa.dfa import DFA
CONST = _Const()

'''
this is to tell us the teacher is treated as a seperate entity 
from the base algorithm, defines base actions of teacher
'''
class SmarterTeacher(Teacher):

    def membership_query(self, test_word):
        return CONST.POS
    
    # returns counter example (in this case None)
    def check_consistency(self, c_minus: DFA, c_plus: DFA):
        return None
    
    # returns counter example (in this case None)
    def equivalence_query(self, proposed_dfa: DFA):
        is_equivalent = True
        return is_equivalent, None


if __name__ == "__main__":
    teacher = SmarterTeacher()
    print(teacher.membership_query("test"))