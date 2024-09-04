
from ..algorithm import Algorithm
from ..common.constants import _Const
from ..common.conjecture_solver import find_solution
from .chen_utils import row_exists_in_main_table, are_rows_equal, find_row_diff, gen_3dfa
from ..teachers.complex_teacher_with_containment import ComplexTeacher

CONST = _Const()

class ChenAlgorithm(Algorithm):

    def run(self, max_dfa_size=None, show_logs=False):
        iterations = 0

        self.total_conjectures = 0
        self.total_clauses = 0
        self.max_clauses = 0

        while iterations < CONST.MAX_ITERATION_COUNT:
            self.make_initial_conjecture()
            tdfa = gen_3dfa(self.obs_table)
            c_plus = tdfa.get_c_plus()
            c_minus = tdfa.get_c_minus()
            counter_example = self.teacher.check_consistency(c_minus=c_minus, c_plus=c_plus)
            if counter_example is None:
                proposed_dfa, (total_clauses_considered, max_clauses, total_conjectures_made) = find_solution(self.obs_table, 
                    self.get_s_plus(), 
                    self.get_s_minus(),
                    max_dfa_size=max_dfa_size,
                    show_logs=show_logs)
                
                self.num_calls += 1
                self.total_clauses += total_clauses_considered
                self.max_clauses = max(self.max_clauses, max_clauses)
                self.total_conjectures += total_conjectures_made

                is_correct, counter_example = self.teacher.equivalence_query(proposed_dfa)
                if is_correct:
                    print("DFA Found and Validated Successfully!")
                    proposed_dfa.print_parameters()
                    return
                self.add_counter_example(counter_example)
            else:
                self.add_counter_example(counter_example)

            iterations += 1
        print("Tried so hard, and got so far, but in the end, it didnt even matter")


    def make_initial_conjecture(self):
        is_closed, prefix_to_add = self.is_obs_table_closed()
        is_consistent, suffix_to_add = self.is_obs_table_consistent()
        while (not is_closed) or (not is_consistent):
            if (not is_consistent):
                self.obs_table.add_suffix(suffix_to_add)
            elif (not is_closed):
                self.obs_table.add_prefix(prefix_to_add)
            is_closed, prefix_to_add = self.is_obs_table_closed()
            is_consistent, suffix_to_add = self.is_obs_table_consistent()

    def get_s_plus(self):
        s_plus = set()
        for prefix in self.obs_table.main_table:
            for suffix in self.obs_table.suffix_set:
                if self.obs_table.main_table[prefix][suffix] == CONST.POS:
                    s_plus.add(prefix + suffix)
        return s_plus

    def get_s_minus(self):
        s_minus = set()
        for prefix in self.obs_table.main_table:
            for suffix in self.obs_table.suffix_set:
                if self.obs_table.main_table[prefix][suffix] == CONST.NEG:
                    s_minus.add(prefix + suffix)
        return s_minus
    

    '''
    The observation table is closed if: 
        for every node at the periphery (extended table nodes)
            there exists atleast one row in the main table that is equal
        i.e. any outgoing connections in the state machine from the prefix set
        can be mapped to another state (another node in the prefix set)

    Returns tuple (is_closed, prefix_to_be_added) 
    where prefix_to_be_added needs to be added to prefix_set if not closed
    '''
    def is_obs_table_closed(self):
        extended_table_component = self.obs_table.extended_table_component
        for prefix in extended_table_component:
            if row_exists_in_main_table(
                extended_table_component[prefix], self.obs_table):
                continue
            else:
                return False, prefix
        return True, None    

    '''
    The observation table is consistent if:
        given two "equal" rows with definers prefix_1 and prefix_2,
        every outgoing node(state) pair based on the same letter is also similar
    
    Returns tuple (is_consistent, suffix_to_be_added) 
    where suffix_to_be_added needs to be added to suffix_set if not consistent
    '''
    def is_obs_table_consistent(self):
        prefix_set = self.obs_table.prefix_set
        num_prefixes = len(prefix_set)
        main_table = self.obs_table.main_table
        alphabet = self.obs_table.alphabet

        for i in range(num_prefixes):
            prefix_1 = prefix_set[i]
            for j in range(i+1, num_prefixes):
                prefix_2 = prefix_set[j]

                if are_rows_equal(main_table[prefix_1], 
                                    main_table[prefix_2]):
                    for letter in alphabet:
                        different_suffix = find_row_diff(
                            main_table[prefix_1 + letter], 
                            main_table[prefix_2 + letter])
                        
                        if different_suffix is None:
                            continue
                        else:
                            return False, letter + different_suffix
        return True, None


if __name__ == "__main__":
    chen_algorithm = ChenAlgorithm(alphabet=['0', '1'], teacher=ComplexTeacher())
    chen_algorithm.run()
    print(chen_algorithm.num_calls)
    print(chen_algorithm.total_clauses)
    print(chen_algorithm.max_clauses)
    print(chen_algorithm.total_conjectures)



