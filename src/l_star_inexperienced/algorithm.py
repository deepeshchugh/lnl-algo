'''
Main points about glp algorithm:
-> L* modified for weakly closed and weakly consistent criteria
->
'''
from .dfa.dfa import DFA
from .common.constants import _Const
from .common.observation_table import ObsTable
from .teachers.smarter_teacher import SmarterTeacher
from .teachers.test_teacher_complex import ComplexTeacher
CONST = _Const()

class Algorithm:
    
    '''
    Initiates Algorithm object with observation table object in first step
    '''
    def __init__(self, alphabet, teacher: SmarterTeacher, prefix_set=None, suffix_set=None):
        if prefix_set is None:
            prefix_set =  [CONST.EMPTY]
        if suffix_set is None:
            suffix_set = [CONST.EMPTY]
        self.teacher = teacher
        self.obs_table = ObsTable(prefix_set, suffix_set, alphabet, teacher=teacher)
        self.obs_table.populate_tables()
        self.num_calls = 0

    # Returns a valid DFA if found.
    def run(self, max_dfa_size=None, show_logs=False) -> DFA: 
        return None

    def add_counter_example(self, word):
        word_array = [""]
        for char in word:
            word_array.append(char)
            self.obs_table.add_prefix(''.join(word_array))



if __name__ == "__main__":
    algorithm = Algorithm(alphabet=['0', '1'], teacher=ComplexTeacher())
    result = algorithm.run()
    print(result)
    print(algorithm.num_calls)


