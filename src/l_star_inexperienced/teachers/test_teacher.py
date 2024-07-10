from ..common.constants import _Const
from ..dfa.dfa import DFA
from .teacher import Teacher
import random
CONST = _Const()

'''
this is to tell us the teacher is treated as a seperate entity 
from the base algorithm, defines base actions of teacher
'''
class TestTeacher(Teacher):

    def membership_query(self, test_word):
        zero_count = 0
        one_count = 0
        if test_word == '':
            return CONST.POS
        for char in test_word:
            if char is '0':
                zero_count += 1
            elif char is '1':
                one_count += 1
        if zero_count%2 == 0:
            return CONST.POS
        else:
            return CONST.NEG
    
    def equivalence_query(self, proposed_dfa: DFA):
        if self.check_dfa(proposed_dfa):
            return True, None
        return False, self.find_counterexample(proposed_dfa)
    
    def find_counterexample(self, proposed_dfa: DFA):
        itr = 0
        while itr < CONST.MAX_COUNTEREXAMPLE_ATTEMPT:
            random_word = self.get_random_word()
            if proposed_dfa.is_word_accepted(random_word) != \
                self.is_valid(random_word):
                return random_word
            itr += 1
        print("Error! couldnt find a counterexample!!!!")
    
    def is_valid(self, test_word):
        state = self.membership_query(test_word)
        if state == CONST.NEG:
            return False
        return True
    
    def get_random_word(self):
        word_array = [""]
        end_reached = False
        while not end_reached:
            new_char = random.randint(0, 2)
            if new_char == 2:
                end_reached == True
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


if __name__ == "__main__":
    teacher = Teacher()
    print(teacher.membership_query("test"))