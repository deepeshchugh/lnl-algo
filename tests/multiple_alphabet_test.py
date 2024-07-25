from l_star_inexperienced.common.constants import _Const # type: ignore
from l_star_inexperienced.dfa.dfa import DFA # type: ignore
from l_star_inexperienced.grinchtein_et_al.glp_algorithm import GlpAlgorithm
from teachers.smarter_teacher import SmarterTeacher # type: ignore
ITER_LIMIT = 1000

import random
CONST = _Const()

class MultiAlphabetTeacher(SmarterTeacher):
    
    def __init__(self):
        print("Initialized")
    
    def membership_query(self, test_word):
        a_count = 0
        b_count = 0
        c_count = 0
        for char in test_word:
            if char == 'a':
                a_count += 1
            elif char == 'b':
                b_count += 1
            elif char == 'c':
                c_count += 1
        if a_count%3 == 0 and b_count%3 == 0:
            return CONST.POS
        if a_count%3 == 0 and b_count%3 != 0:
            return CONST.NEG
        elif a_count%3 == 1 and c_count%3 == 0:
            return CONST.NEG
        else:
            return CONST.DONT_CARE
        
    def equivalence_query(self, proposed_dfa: DFA):
        counter_example = self.find_counterexample(proposed_dfa=proposed_dfa)
        if counter_example is None:
            return True, None
        return False, counter_example
    
    def find_counterexample(self, proposed_dfa: DFA):
        itr = 0
        while itr < ITER_LIMIT:
            print(itr)
            random_word = self.get_random_word()
            if self.is_valid(random_word) is None:
                itr += 1
                continue
            if proposed_dfa.is_word_accepted(random_word) != \
                self.is_valid(random_word):
                return random_word
            itr += 1
        # print("couldn't find a counterexample so presuming solved")
        return None
    
    def is_valid(self, test_word):
        state = self.membership_query(test_word)
        if state == CONST.NEG:
            return False
        if state == CONST.POS:
            return True
        return None
    
    def get_random_word(self):
        word_array = [""]
        end_reached = False
        while not end_reached:
            new_char = random.randint(0, 3)
            if new_char == 3:
                end_reached = True
            elif new_char == 0:
                word_array.append('a')
            elif new_char == 1:
                word_array.append('b')
            elif new_char == 2:
                word_array.append('c')
        return ''.join(word_array)
        
glp = GlpAlgorithm(alphabet=['a', 'b', 'c'], teacher=MultiAlphabetTeacher())
result_dfa = glp.run(show_logs=True)
result_dfa.visualize()
print(glp.num_calls)
print(glp.total_clauses)
print(glp.max_clauses)
print(glp.total_conjectures)
