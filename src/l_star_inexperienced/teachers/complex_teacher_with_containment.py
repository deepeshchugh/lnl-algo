from ..common.constants import _Const
from ..dfa.dfa import DFA
from ..teachers.smarter_teacher import SmarterTeacher
CONST = _Const()

'''
this is to tell us the teacher is treated as a seperate entity 
from the base algorithm, defines base actions of teacher
'''
class ComplexTeacher(SmarterTeacher):
    
    def __init__(self):
        self.count = 0
        self.initialize_accepting_fa()
        self.initialize_rejecting_fa()
        self.alphabet = {'0', '1'}
    
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
        counter_example = self.find_counterexample(proposed_dfa=proposed_dfa)
        if counter_example is None:
            return True, None
        return False, counter_example
    
    def find_counterexample(self, proposed_dfa: DFA):
        proposed_consumes_actual, counter_example = self.check_accepting_language(proposed_fa=proposed_dfa)
        if not proposed_consumes_actual:
            return counter_example
        proposed_consumes_actual, counter_example = self.check_rejecting_language(proposed_fa=proposed_dfa)
        return counter_example
    
    def is_valid(self, test_word):
        state = self.membership_query(test_word)
        if state == CONST.NEG:
            return False
        if state == CONST.POS:
            return True
        return None

    def check_consistency(self, c_minus: DFA, c_plus: DFA):
        c_minus_passes, counter_example = \
            self.check_consistency_c_minus(c_minus=c_minus)
        if not c_minus_passes:
            return counter_example
        c_plus_passes, counter_example = \
            self.check_consistency_c_plus(c_plus=c_plus)    
        return counter_example
    
    def check_consistency_c_minus(self, c_minus: DFA):
        state_pairs_checked = []
        a_fs = c_minus.first_state
        b_fs = self.accepting_fa.first_state
        return self.dfs_check_a_subset_b(
            fa_a=c_minus,
            fa_b=self.accepting_fa,
            state_a=a_fs,
            state_b=b_fs,
            state_pairs_checked=state_pairs_checked
        )
    
    def check_consistency_c_plus(self, c_plus: DFA):
        state_pairs_checked = []
        a_fs = c_plus.first_state
        b_fs = self.rejecting_fa.first_state


        return self.dfs_check_abar_subset_b(
            fa_a=c_plus,
            fa_b=self.rejecting_fa,
            state_a=a_fs,
            state_b=b_fs,
            state_pairs_checked=state_pairs_checked
        )
    
    def check_accepting_language(self, proposed_fa: DFA):
        state_pairs_checked = []
        proposed_fs = proposed_fa.first_state
        actual_fs = self.accepting_fa.first_state
        return self.dfs_check_a_subset_b(
            fa_a=self.accepting_fa,
            fa_b=proposed_fa,
            state_a=actual_fs,
            state_b=proposed_fs,
            state_pairs_checked=state_pairs_checked
        )
    
    def check_rejecting_language(self, proposed_fa: DFA):
        state_pairs_checked = []
        proposed_fs = proposed_fa.first_state
        actual_fs = self.rejecting_fa.first_state
        return self.dfs_check_a_subset_bbar(
            fa_a=self.rejecting_fa,
            fa_b=proposed_fa,
            state_a=actual_fs,
            state_b=proposed_fs,
            state_pairs_checked=state_pairs_checked
        )

    def dfs_check_a_subset_b(self, fa_a: DFA, fa_b: DFA, state_a, state_b, state_pairs_checked: list):
        if (state_a, state_b) in state_pairs_checked:
            return (True, None)
        # a subset b equals to if accepted in a implies accepted b and not vice versa
        if fa_a.is_state_final(state_a) and not fa_b.is_state_final(state_b):
            return (False, "")
        state_pairs_checked.append((state_a, state_b))
        
        for char in self.alphabet:
            isChainValid, transition_ce = self.dfs_check_a_subset_b(
                fa_a=fa_a,
                fa_b=fa_b,
                state_a=fa_a.delta[state_a][char],
                state_b=fa_b.delta[state_b][char],
                state_pairs_checked=state_pairs_checked)
            if not isChainValid:
                return (False, char + transition_ce)
        return True, None
    
    def dfs_check_abar_subset_b(self, fa_a: DFA, fa_b: DFA, state_a, state_b, state_pairs_checked: list):
        if (state_a, state_b) in state_pairs_checked:
            return (True, None)
        # abar subset b equals to if rejected in a implies accepted b and not vice versa
        if not fa_a.is_state_final(state_a) and not fa_b.is_state_final(state_b):
            return (False, "")
        state_pairs_checked.append((state_a, state_b))
        
        for char in self.alphabet:
            isChainValid, transition_ce = self.dfs_check_abar_subset_b(
                fa_a=fa_a,
                fa_b=fa_b,
                state_a=fa_a.delta[state_a][char],
                state_b=fa_b.delta[state_b][char],
                state_pairs_checked=state_pairs_checked)
            if not isChainValid:
                return (False, char + transition_ce)
        return True, None
    
    def dfs_check_a_subset_bbar(self, fa_a: DFA, fa_b: DFA, state_a, state_b, state_pairs_checked: list):
        if (state_a, state_b) in state_pairs_checked:
            return (True, None)
        # a subset bbar equals to if accepted in a implies rejected b and not vice versa
        if fa_a.is_state_final(state_a) and fa_b.is_state_final(state_b):
            return (False, "")
        state_pairs_checked.append((state_a, state_b))
        
        for char in self.alphabet:
            isChainValid, transition_ce = self.dfs_check_a_subset_bbar(
                fa_a=fa_a,
                fa_b=fa_b,
                state_a=fa_a.delta[state_a][char],
                state_b=fa_b.delta[state_b][char],
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

print(ComplexTeacher().membership_query("0"))
    
