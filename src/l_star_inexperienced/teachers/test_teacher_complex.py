from ..common.constants import _Const
from ..dfa.dfa import DFA
from .teacher import Teacher
import random
CONST = _Const()

'''
this is to tell us the teacher is treated as a seperate entity 
from the base algorithm, defines base actions of teacher
'''
class ComplexTeacher(Teacher):
    
    def __init__(self):
        self.alphabet = {'0', '1'}
        self.initialize_accepting_fa()
        self.initialize_rejecting_fa()
    
    def membership_query(self, test_word):
        zero_count = 0
        one_count = 0
        if test_word == '':
            return CONST.POS
        for char in test_word:
            if char == '0':
                zero_count += 1
            elif char == '1':
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
        counter_example = self.find_counterexample(proposed_dfa=proposed_dfa)
        formal_counter_example = self.find_counterexample_formal(proposed_dfa=proposed_dfa)
        if counter_example is None and formal_counter_example is not None:
            print("ERROR ERROR Conflicting Example States")
            print("Formal counter:", formal_counter_example)
            proposed_dfa.visualize()
            raise RuntimeError("Check for conflict")
        if counter_example is not None and formal_counter_example is None:
            print("ERROR ERROR Conflicting Example States case 2")
            print(counter_example)
            proposed_dfa.visualize()
            raise RuntimeError("Check for conflict")
        if counter_example is None:
            return True, None
        return False, counter_example
    
    def find_counterexample_formal(self, proposed_dfa: DFA):
        proposed_subsumes_actual, counter_example = self.check_accepting_language(proposed_fa=proposed_dfa)
        if not proposed_subsumes_actual:
            return counter_example
        proposed_subsumes_actual, counter_example = self.check_rejecting_language(proposed_fa=proposed_dfa)
        return counter_example
    
    def find_counterexample(self, proposed_dfa: DFA):
        itr = 0
        while itr < CONST.MAX_COUNTEREXAMPLE_ATTEMPTS:
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
            new_char = random.randint(0, 2)
            if new_char == 2:
                end_reached = True
            else:
                word_array.append(str(new_char))
        return ''.join(word_array)

    def check_accepting_language(self, proposed_fa: DFA):
        state_pairs_checked = []
        proposed_fs = proposed_fa.first_state
        actual_fs = self.accepting_fa.first_state
        return self.dfs_check_accepting(
            proposed_fa=proposed_fa,
            actual_fa=self.accepting_fa,
            proposed_state=proposed_fs,
            actual_state=actual_fs,
            state_pairs_checked=state_pairs_checked
        )
    
    def check_rejecting_language(self, proposed_fa: DFA):
        state_pairs_checked = []
        proposed_fs = proposed_fa.first_state
        actual_fs = self.rejecting_fa.first_state
        return self.dfs_check_rejecting(
            proposed_fa=proposed_fa,
            actual_fa=self.rejecting_fa,
            proposed_state=proposed_fs,
            actual_state=actual_fs,
            state_pairs_checked=state_pairs_checked
        )

    def dfs_check_accepting(self, proposed_fa: DFA, actual_fa: DFA, proposed_state, actual_state, state_pairs_checked: list):
        if (proposed_state, actual_state) in state_pairs_checked:
            return (True, None)
        if actual_fa.is_state_final(actual_state) and not proposed_fa.is_state_final(proposed_state):
            return (False, "")
        state_pairs_checked.append((proposed_state, actual_state))
        
        for char in self.alphabet:
            isChainValid, transition_ce = self.dfs_check_accepting(
                proposed_fa=proposed_fa,
                actual_fa=actual_fa,
                proposed_state=proposed_fa.delta[proposed_state][char],
                actual_state=actual_fa.delta[actual_state][char],
                state_pairs_checked=state_pairs_checked)
            if not isChainValid:
                return (False, char + transition_ce)
        return True, None
    
    def dfs_check_rejecting(self, proposed_fa: DFA, actual_fa: DFA, proposed_state, actual_state, state_pairs_checked: list):
        if (proposed_state, actual_state) in state_pairs_checked:
            return (True, None)
        if actual_fa.is_state_final(actual_state) and proposed_fa.is_state_final(proposed_state):
            return (False, "")
        state_pairs_checked.append((proposed_state, actual_state))
        
        for char in self.alphabet:
            isChainValid, transition_ce = self.dfs_check_rejecting(
                proposed_fa=proposed_fa,
                actual_fa=actual_fa,
                proposed_state=proposed_fa.delta[proposed_state][char],
                actual_state=actual_fa.delta[actual_state][char],
                state_pairs_checked=state_pairs_checked)
            if not isChainValid:
                return (False, char + transition_ce)
        
        return True, None
    
    
    def initialize_accepting_fa(self):
        delta = {}
        delta[1] = {'0':2,'1':1}
        delta[2] = {'0':3,'1':2}
        delta[3] = {'0':1,'1':3}

        self.accepting_fa = DFA(
        num_states=3,
        alphabet=['0', '1'],
        delta=delta,
        final_states=set([1]),
        first_state=1
    )
        
    def initialize_rejecting_fa(self):
        delta = {}
        delta[1] = {'0':4,'1':2}
        delta[2] = {'0':5,'1':3}
        delta[3] = {'0':6,'1':1}
        delta[4] = {'0':7,'1':5}
        delta[5] = {'0':7,'1':6}
        delta[6] = {'0':7,'1':4}
        delta[7] = {'0':7,'1':7}

        self.rejecting_fa = DFA(
        num_states=7,
        alphabet=['0', '1'],
        delta=delta,
        final_states=set([4]),
        first_state=1
    )
        
    
