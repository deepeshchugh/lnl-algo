'''
Main points about glp algorithm:
-> L* modified for weakly closed and weakly consistent criteria
->
'''
from constants import _Const

class ObsTable:
    def __init__(self, test_param):
        self.main_table = {}
        self.prefix_set = []
        self.suffix_set = []
        self.alphabet = []

    # Default behaviour for now
    def is_closed(self):
        return True
    
    # Default behaviour for now
    def is_consistent(self):
        return True
    
    # Needs to send inorder tuple list (prefix, membership)
    def gen_membership_queries(self):
        return []

    # Takes membership query responses to generate new iteration of obs table
    def gen_new_table(self, prefix, membership_query, membership_responses):
        return self.main_table
    
CONST = _Const()
print(CONST.POS)