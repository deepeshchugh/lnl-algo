import random
from l_star_inexperienced.dfa import DFA

MAX_STATES = 10
MAX_SWITCHES = 10

def is_rand_true(percent_chance):
    return random.randrange(100) < percent_chance

def has_orphans(delta, last_state, charset):
    num_states = last_state
    first_state = 1
    states_reached = dfs_check_orphans(
        state=first_state,
        checked=set(),
        charset=charset,
        delta=delta
    )
    if len(states_reached) == num_states:
        return False
    return True
    
def dfs_check_orphans(state, checked : set, charset, delta) -> set:
    if state in checked:
        return {}
    new_set = {state}
    checked.add(state)
    for char in charset:
        new_set = new_set.union(dfs_check_orphans(
            state=delta[state][char],
            checked=checked,
            charset=charset,
            delta=delta
        ))
    return new_set

def do_switches(old_delta, last_state, charset):
    for _ in range(MAX_SWITCHES):
        state_1 = random.randrange(last_state) + 1
        state_2 = random.randrange(last_state) + 1
        char_1 = random.choice(charset)
        char_2 = random.choice(charset)
        state_1_char_1_old_val = old_delta[state_1][char_1]
        old_delta[state_1][char_1] = old_delta[state_2][char_2]
        old_delta[state_2][char_2] = state_1_char_1_old_val
        if has_orphans(delta=old_delta, last_state=last_state, charset=charset):
            old_delta[state_2][char_2] = old_delta[state_1][char_1]
            old_delta[state_1][char_1] = state_1_char_1_old_val
    return old_delta

def get_final_states(num_states):
    num_final = random.randrange(1,num_states)
    final_states = set()
    for i in range(num_final):
        final_states.add(random.randrange(1,num_states))
    return final_states

def gen_random_dfa():
    charset = ['0', '1']
    delta = {}
    last_state_probability = 0
    reflexive_probability = 15
    found_last_state = False
    current_state_count = 0
    while not found_last_state:
        new_state = current_state_count+1
        current_state_count += 1
        found_last_state = True
        new_delta = {}
        for char in charset:
            if not is_rand_true(last_state_probability):
                new_delta[char] = new_state+1
                found_last_state = False
            elif is_rand_true(reflexive_probability):
                new_delta[char] = new_state
            else:
                new_delta[char] = random.randrange(new_state-1)+1
        last_state_probability += 13
        delta[new_state] = new_delta
    last_derived_state = current_state_count
    updated_delta = do_switches(delta, last_derived_state, charset)
    final_states = get_final_states(num_states=current_state_count)
    dfa = DFA(
        num_states=current_state_count,
        alphabet=charset,
        delta=updated_delta,
        final_states=final_states,
        first_state=1
    )
    return dfa

def gen_rejecting_dfa(accepting_dfa : DFA):
    final_states = set()
    possible_states = []
    for state in range(1, accepting_dfa.num_states+1):
        if state in accepting_dfa.final_states:
            continue
        possible_states.append(state)
    for i in range(len(possible_states)):
        final_states.add(random.choice(possible_states))
    return DFA(
        num_states=accepting_dfa.num_states,
        alphabet=accepting_dfa.alphabet,
        delta=accepting_dfa.delta,
        final_states=final_states,
        first_state=1
    )


from l_star_inexperienced.common.constants import _Const # type: ignore
from l_star_inexperienced.dfa.dfa import DFA # type: ignore
from l_star_inexperienced.grinchtein_et_al.glp_algorithm import GlpAlgorithm
from l_star_inexperienced.teachers.smarter_teacher import SmarterTeacher
from l_star_inexperienced.leucker_et_al.lnl import LNLAlgorithm # type: ignore
ITER_LIMIT = 1000

import random
CONST = _Const()

class TeacherE(SmarterTeacher):
    
    def __init__(self, accepting_fa:DFA =None, rejecting_fa:DFA=None):
        self.alphabet = {'0','1'}
        if accepting_fa is None and rejecting_fa is None:
            accepting_fa = gen_random_dfa()
            rejecting_fa = gen_rejecting_dfa(accepting_dfa=accepting_fa)
        self.accepting_fa = accepting_fa
        self.rejecting_fa = rejecting_fa
    
    def membership_query(self, test_word):
        if self.accepting_fa.is_word_accepted(test_word):
            return CONST.POS
        elif self.rejecting_fa.is_word_accepted(test_word):
            return CONST.NEG
        else:
            return CONST.DONT_CARE
        
    def equivalence_query(self, proposed_dfa: DFA):
        counter_example = None
        try:
            counter_example = self.find_counterexample_formal(proposed_dfa=proposed_dfa)
        except:
            self.accepting_fa.print_parameters()
            self.rejecting_fa.print_parameters()
            proposed_dfa.print_parameters()
            raise Exception("Something happened")
        if counter_example is None:
            return True, None
        return False, counter_example
    
    def check_consistency(self, c_minus: DFA, c_plus: DFA):
        counter_example = None
        try:
            c_minus_passes, counter_example = \
            self.check_consistency_c_minus(c_minus=c_minus)
            if not c_minus_passes:
                return counter_example
            c_plus_passes, counter_example = \
                self.check_consistency_c_plus(c_plus=c_plus)
        except:
            self.accepting_fa.print_parameters()
            self.rejecting_fa.print_parameters()
            c_plus.print_parameters()
            c_minus.print_parameters()
            raise Exception("Something happened")    
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

def get_teachere_instance() -> DFA:
    accepting_dfa = gen_random_dfa()
    rejecting_dfa = gen_rejecting_dfa(accepting_dfa=accepting_dfa)
    return TeacherE(accepting_fa=accepting_dfa, rejecting_fa=rejecting_dfa)

if __name__ == '__main__':
    lnl = LNLAlgorithm(alphabet=['0', '1'], teacher=get_teachere_instance())
    result_dfa = lnl.run(show_logs=True)

    result_dfa.visualize()
    lnl.teacher.accepting_fa.print_parameters()
    lnl.teacher.rejecting_fa.print_parameters()