'''
Main points about glp algorithm:
-> L* modified for weakly closed and weakly consistent criteria
->
'''
from constants import _Const
from glp_utils import similar_row_exists
CONST = _Const()

# dummy function TODO replace
def mem_query(string):
    if string == '00':
        return CONST.POS
    if string == '01':
        return CONST.DONT_CARE
    return CONST.NEG



class ObsTable:
    def __init__(self, prefix_set, suffix_set, alphabet):
        self.main_table = {}
        self.extended_table_component = {}
        self.prefix_set = prefix_set
        self.suffix_set = suffix_set
        self.alphabet = alphabet

    # Default behaviour for now
    def is_closed(self):
        for prefix in self.extended_table_component:
            if similar_row_exists(self.extended_table_component[prefix], self):
                continue
            else:
                return False, prefix
        return True, ""
    


    # Default behaviour for now
    def is_consistent(self):
        return True
    
    # Needs to send inorder tuple list (prefix, membership)
    def gen_membership_queries(self):
        return []

    # First generate a base main table
    def gen_new_table(self):
        main_table = {}
        extended_table_component = {}
        for prefix in self.prefix_set:
            main_table[prefix] = self.gen_obs_table_row(prefix)
        for prefix in self.prefix_set:
            for letter in self.alphabet:
                if (prefix + letter) not in self.prefix_set:
                    suffix_row = self.gen_obs_table_row(prefix + letter)
                    main_table[prefix + letter] = suffix_row
                    extended_table_component[prefix + letter] = suffix_row
        self.main_table = main_table
        self.extended_table_component = extended_table_component
        return main_table
    
    def gen_obs_table_row(self, prefix):
        suffix_row = {}
        for suffix in self.suffix_set:
            suffix_row[suffix] = mem_query(prefix + suffix)
        return suffix_row

    # Print current observation table
    def print_table(self):
        print("\t", end='\'')
        print(*self.suffix_set, sep="\'\t\'", end="\'\n")
        for key in self.main_table:
            print("\'" + key, end="\'")
            for suffix in self.suffix_set:
                print("\t", end="")
                print(self.main_table[key][suffix], end="\t")
                print()
    




    


observation_table = ObsTable([CONST.EMPTY, '0'], [CONST.EMPTY], ['0', '1'])
observation_table.gen_new_table()
observation_table.print_table()
print(observation_table.is_closed())