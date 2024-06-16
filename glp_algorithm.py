'''
Main points about glp algorithm:
-> L* modified for weakly closed and weakly consistent criteria
->
'''
from constants import _Const
from observation_table import ObsTable
from glp_utils import similar_row_exists_in_main_table, are_rows_similar, find_row_diff
CONST = _Const()

class GlpAlgorithm:
    
    '''
    Initiates Algorithm object with observation table object in first step
    '''
    def __init__(self, prefix_set, suffix_set, alphabet):
        self.obs_table = ObsTable(prefix_set, suffix_set, alphabet)
        self.obs_table.populate_tables()

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
            there exists atleast one row in the main table that is similar
        i.e. any outgoing connections in the state machine from the prefix set
        can be mapped to another state (another node in the prefix set)

    Returns tuple (is_closed, prefix_to_be_added) 
    where prefix_to_be_added needs to be added to prefix_set if not closed
    '''
    def is_obs_table_closed(self):
        extended_table_component = self.obs_table.extended_table_component
        for prefix in extended_table_component:
            if similar_row_exists_in_main_table(
                extended_table_component[prefix], self.obs_table):
                continue
            else:
                return False, prefix
        return True, None    

    '''
    The observation table is consistent if:
        given two "similar" rows with definers prefix_1 and prefix_2,
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

                if are_rows_similar(main_table[prefix_1], 
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
    glp_algorithm = GlpAlgorithm(
        prefix_set=[CONST.EMPTY, '0', '1'], 
        suffix_set=[CONST.EMPTY], 
        alphabet=['0', '1'])
    print("First GLP Algo Object initialized")
    glp_algorithm.obs_table.print_table()
    print(glp_algorithm.is_obs_table_closed())
    print(glp_algorithm.is_obs_table_consistent())
    print("This is inconsistent because 0 and 1 are similar but 00 and 10 are not")

    glp_algorithm = GlpAlgorithm(
        prefix_set=[CONST.EMPTY], 
        suffix_set=[CONST.EMPTY], 
        alphabet=['0', '1'])
    print("Second GLP Algo Object initialized")
    glp_algorithm.obs_table.print_table()
    print(glp_algorithm.is_obs_table_closed())
    print(glp_algorithm.is_obs_table_consistent())
    # Logic changed, proper things still pending
    print("This is not closed because of extended row 00 not having a match")
    print("Lets try fixing it")
    glp_algorithm.make_initial_conjecture()
    print(glp_algorithm.is_obs_table_closed())
    print(glp_algorithm.is_obs_table_consistent())
    print(glp_algorithm.obs_table.extended_table_component)
    print(glp_algorithm.get_s_plus())
    print(glp_algorithm.get_s_minus())



