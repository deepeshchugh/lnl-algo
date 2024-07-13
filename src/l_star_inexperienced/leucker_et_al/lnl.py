
from ..dfa.dfa import DFA
from ..common.constants import _Const
from ..common.observation_table import ObsTable
from ..common.conjecture_solver import find_solution
# from ..common.alt_conjecture_solver import alt_find_solution as find_solution
from ..teachers.smarter_teacher import SmarterTeacher
from ..teachers.complex_teacher_with_containment import ComplexTeacher

# Reusing chen utility functions
from ..chen_et_al.chen_utils import row_exists_in_main_table, are_rows_equal, find_row_diff, gen_3dfa

CONST = _Const()

class LNLAlgorithm:
    
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

    def run(self) -> DFA:
        iterations = 0
        while iterations < CONST.MAX_ITERATION_COUNT:
            self.make_initial_conjecture()
            tdfa = gen_3dfa(self.obs_table)
            print("Three DFA:")
            tdfa.print_parameters()
            c_plus = tdfa.get_c_plus()
            c_minus = tdfa.get_c_minus()
            counter_example = self.teacher.check_consistency(c_minus=c_minus, c_plus=c_plus)
            if counter_example is None:
                
                #Presuming minimally accepting dfa
                is_correct, counter_example = self.teacher.equivalence_query(c_plus)

                if is_correct:
                    proposed_dfa = find_solution(self.obs_table, 
                    self.get_s_plus(), 
                    self.get_s_minus())
                    print("DFA Found and Validated Successfully!")
                    return proposed_dfa
                    # proposed_dfa.print_parameters()
                self.add_counter_example(counter_example)
            else:
                self.add_counter_example(counter_example)

            iterations += 1
        print("Tried so hard, and got so far, but in the end, it didnt even matter")
        return None
    
    def add_counter_example(self, word):
        word_array = [""]
        for char in word:
            word_array.append(char)
            self.obs_table.add_prefix(''.join(word_array))


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
        print("conjecture:")
        self.obs_table.print_table()

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
    lnl_algorithm = LNLAlgorithm(alphabet=['0', '1'], teacher=ComplexTeacher())
    solution_dfa = lnl_algorithm.run()
    solution_dfa.print_parameters()
    solution_dfa.visualize()



