from l_star_inexperienced.common.constants import _Const # type: ignore
from l_star_inexperienced.dfa.dfa import DFA # type: ignore
from l_star_inexperienced.grinchtein_et_al.glp_algorithm import GlpAlgorithm
from l_star_inexperienced.teachers.smarter_teacher import SmarterTeacher # type: ignore
ITER_LIMIT = 1000

import random
CONST = _Const()

class TeacherB(SmarterTeacher):
    
    def __init__(self):
        self.alphabet = {'a', 'b'}
        self.initialize_accepting_fa()
        self.initialize_rejecting_fa()
    
    def membership_query(self, test_word):
        a_count = 0
        b_count = 0
        for char in test_word:
            if char == 'a':
                a_count += 1
            elif char == 'b':
                b_count += 1
        if a_count%2 == 0 and b_count%2 == 0:
            return CONST.POS
        elif a_count%2 == 1 and b_count%2 == 1:
            return CONST.NEG
        else:
            return CONST.DONT_CARE
        
    def equivalence_query(self, proposed_dfa: DFA):
        counter_example = self.find_counterexample_formal(proposed_dfa=proposed_dfa)
        if counter_example is None:
            return True, None
        return False, counter_example
    
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
    
    def find_counterexample_formal(self, proposed_dfa: DFA):
        proposed_subsumes_actual, counter_example = self.check_accepting_language(proposed_fa=proposed_dfa)
        if not proposed_subsumes_actual:
            return counter_example
        proposed_subsumes_actual, counter_example = self.check_rejecting_language(proposed_fa=proposed_dfa)
        return counter_example

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
            elif new_char == 0:
                word_array.append('a')
            elif new_char == 1:
                word_array.append('b')
        return ''.join(word_array)

    def initialize_accepting_fa(self):
        delta = {}
        delta[1] = {'a':2,'b':3}
        delta[2] = {'a':1,'b':4}
        delta[3] = {'a':4,'b':1}
        delta[4] = {'a':3,'b':2}

        self.accepting_fa = DFA(
        num_states=4,
        alphabet=['a', 'b'],
        delta=delta,
        final_states=set([1]),
        first_state=1
    )
        
    def initialize_rejecting_fa(self):
        delta = {}
        delta[1] = {'a':2,'b':3}
        delta[2] = {'a':1,'b':4}
        delta[3] = {'a':4,'b':1}
        delta[4] = {'a':3,'b':2}

        self.rejecting_fa = DFA(
        num_states=4,
        alphabet=['a', 'b'],
        delta=delta,
        final_states=set([4]),
        first_state=1
    )
    
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
    
if __name__ == '__main__':
    glp = GlpAlgorithm(alphabet=['a', 'b'], teacher=TeacherB())
    result_dfa = glp.run(show_logs=True)
    result_dfa.visualize()
    # TeacherB().rejecting_fa.visualize()
    print(glp.num_calls)
    print(glp.total_clauses)
    print(glp.max_clauses)
    print(glp.total_conjectures)
