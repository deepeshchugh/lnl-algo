from constants import _Const
from observation_table_utils import gen_obs_table_row
from test_teacher import TestTeacher
CONST = _Const()

'''
Has 5 main components:
    prefix_set      : current set of prefixes i.e. row definers in obs table
    suffix_set      : current set of suffixes i.e. col definers in obs table
    alphabet        : the set of smallest components of the language in which the dfa is defined (i.e. what a step in the corresponding dfa is)
    main_table      : will contain the obs table value for all combos of prefix + suffix set entities
                      Additionally contains all of the extended table component(This is a dict/map)
    extended_table(_component)  : contains only the "new" rows from main table i.e. those row definers generated by combining prefixes and letters 
                      (excluding combos which already exist in the prefix_set) (This is a dict/map)
'''
class ObsTable:

    '''
    Initiates obs table object without populating main and extended tables.
    '''
    def __init__(self, prefix_set, suffix_set, alphabet, teacher):
        self.main_table = {}
        self.extended_table_component = {}
        if CONST.EMPTY not in prefix_set:
            prefix_set.append(CONST.EMPTY)
        self.prefix_set = prefix_set
        self.suffix_set = suffix_set
        self.alphabet = alphabet
        self.teacher = teacher

    '''
    Populates main table and extended table component based on 
    prefixes, suffixes and alphabet
    '''
    def populate_tables(self):
        self.main_table = {}
        self.extended_table_component = {}

        self.populate_base_table()
        self.populate_extended_table_component()
    
    def populate_base_table(self):
        for prefix in self.prefix_set:
            self.main_table[prefix] =\
                gen_obs_table_row(prefix, self.suffix_set, self.teacher)

    def populate_extended_table_component(self):
        for prefix in self.prefix_set:
            for letter in self.alphabet:
                if (prefix + letter) not in self.prefix_set:
                    new_row = gen_obs_table_row(prefix + letter, 
                                                self.suffix_set,
                                                self.teacher)
                    self.main_table[prefix + letter] = new_row
                    self.extended_table_component[prefix + letter] = new_row

    # Add prefix and regenerate the two tables.
    def add_prefix(self, prefix):
        if prefix in self.prefix_set:
            return
        
        self.prefix_set.append(prefix)

        # optimized in a previous commit, opting for simplicity for now
        self.populate_tables()
    
    # Add suffix and regenerate the two tables.
    def add_suffix(self, suffix):
        if suffix in self.suffix_set:
            #TODO add error here
            print("suffix already exists in obs table")
            return
        
        self.suffix_set.append(suffix)

        # optimized in a previous commit, opting for simplicity for now
        self.populate_tables()

    ''' 
    Prints current observation table (main_table), no other functionality.
    '''
    def print_table(self):
        print("\t", end='\'')
        print(*self.suffix_set, sep="\'\t\'", end="\'\n")
        for key in self.main_table:
            print("\'" + key, end="\'")
            for suffix in self.suffix_set:
                print("\t", end="")
                print(self.main_table[key][suffix], end="")
            print()


if __name__ == "__main__":
    observation_table = ObsTable(
        prefix_set=[CONST.EMPTY, '0', '1'], 
        suffix_set=[CONST.EMPTY], 
        alphabet=['0', '1'],
        teacher=TestTeacher())
    observation_table.populate_tables()
    observation_table.print_table()
    observation_table.add_prefix('00')
    observation_table.add_suffix('1')
    observation_table.print_table()