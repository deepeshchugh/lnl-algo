from constants import _Const
from dfa import DFA
from teacher import Teacher
import random
CONST = _Const()

'''
this is to tell us the teacher is treated as a seperate entity 
from the base algorithm, defines base actions of teacher
'''
class ComplexTeacher(Teacher):
    
    def __init__(self):
        self.count = 0

    def membership_query(self, test_word):
        zero_count = 0
        one_count = 0
        if test_word == '':
            return CONST.DONT_CARE
        for char in test_word:
            if char is '0':
                zero_count += 1
            elif char is '1':
                one_count += 1
        if zero_count%3 == 0:
            return CONST.POS
        elif zero_count == 1 and one_count%3 == 0:
            return CONST.NEG
        else:
            return CONST.DONT_CARE
        
    def equivalence_query(self, proposed_dfa: DFA):
        # if self.check_dfa(proposed_dfa):
        #     return True, None
        counter_example = self.find_counterexample(proposed_dfa)
        if counter_example is None:
            return True, None
        return False, counter_example
    
    def find_counterexample(self, proposed_dfa: DFA):
        itr = 0
        while itr < CONST.MAX_ITERATION_COUNT:
            random_word = self.get_random_word()
            if self.is_valid(random_word) is None:
                itr += 1
                continue
            if proposed_dfa.is_word_accepted(random_word) != \
                self.is_valid(random_word):
                return random_word
            itr += 1
        print("couldn't find a counterexample so presuming solved")
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
            new_char = random.randint(0, 2)
            if new_char == 2:
                end_reached = True
            else:
                word_array.append(str(new_char))
        return ''.join(word_array)

    def check_dfa(self, proposed_dfa: DFA):
        if proposed_dfa.num_states != 2:
            return False
        if len(proposed_dfa.final_states) != 1:
            return False
        valid_state = list(proposed_dfa.final_states)[0]
        invalid_state = 3 - valid_state

        if proposed_dfa.delta[valid_state]['0'] != invalid_state:
            return False
        if proposed_dfa.delta[valid_state]['1'] != valid_state:
            return False
        if proposed_dfa.delta[invalid_state]['0'] != valid_state:
            return False
        if proposed_dfa.delta[invalid_state]['1'] != invalid_state:
            return False
        if proposed_dfa.first_state == valid_state:
            return True
        return False
