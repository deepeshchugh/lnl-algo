'''
This module responsible for encoding a given conjecture into
its given cnf form, matching the glp constraints and attempting to 
find a solution using naive iteration 
(ignoring binary search recommendation for now)
'''

from observation_table import ObsTable
from constants import _Const
from glp_algorithm import GlpAlgorithm
from pycryptosat import Solver

CONST = _Const()


'''
Primary external function of this module
i/p: Observation Table, S Plus Set, S Minus Set
o/p: Minimal DFA Object matching constraint
TODO Make DFA Class and corresponding encoding conversion
'''
def find_solution(obsTable: ObsTable, s_plus: set, s_minus: set):
    n = 1
    while n <= CONST.MAX_DFA_SIZE:
        foundDFA, DFA = find_dfa_with_size(obsTable=obsTable, 
                        s_plus=s_plus, s_minus=s_minus, 
                        num_states=n)
        if foundDFA:
            print("Found at n = ", n)
            return foundDFA, DFA
        n+=1
    if n > CONST.MAX_DFA_SIZE:
        print("Error, not able to find DFA within given constraints")

'''
One iteration of sat solver
takes i/p: obsTable, s plus set, s minus set, number of states
o/p: foundDFA: boolean, DFA TODO
Adds clauses according to the four constraints provided in glp sat based approach
'''
def find_dfa_with_size(obsTable: ObsTable, s_plus: set, s_minus: set, num_states):
    total_words = len(s_minus) + len(s_plus)
    alphabet = obsTable.alphabet

    combined_words = set()
    for item in s_plus:
        combined_words.add(item)
    for item in s_minus:
        combined_words.add(item)
    if total_words != len(combined_words):
        print("These sets are supposed to be disjoint!! ERROR!")
    
    s = Solver()

    item_state_map = {}
    item_increment = 0
    for item in combined_words:
        state_list = []
        for i in range(1, num_states+1):
            state_list.append(item_increment + i)
        item_state_map[item] = state_list
        item_increment += num_states
    
    # Clause 1
    for item in combined_words:
        clause_list = []
        for i in range(0, num_states):
            clause_list.append(item_state_map[item][i])
        s.add_clause(clause_list)
    
    # Clause 2
    for item in combined_words:
        for i in range(0, num_states-1):
            for j in range(i+1, num_states):
                s.add_clause([-1 * item_state_map[item][i], 
                              -1 * item_state_map[item][j]])
    
    # Clause 3
    for item_1 in combined_words:
        for item_2 in combined_words:
            if item_1 == item_2:
                continue
            for letter in alphabet:
                if item_1 + letter in combined_words:
                    if item_2 + letter in combined_words:
                        for i in range(0, num_states-1):
                            for j in range(0, num_states-1):
                                s.add_clause([-1 * item_state_map[item_1][i], 
                                              -1 * item_state_map[item_2][j], 
                                              -1 * item_state_map[item_1 + letter][j], 
                                              item_state_map[item_2 + letter][j]])
                                s.add_clause([-1 * item_state_map[item_1][i], 
                                              -1 * item_state_map[item_2][j], 
                                              item_state_map[item_1 + letter][j], 
                                              -1 * item_state_map[item_2 + letter][j]])

    # Clause 4
    for item_1 in s_plus:
        for item_2 in s_minus:
            for i in range(0, num_states):
                s.add_clause([-1 * item_state_map[item_1][i], -1 * item_state_map[item_2][i]])
    
    sat, solution = s.solve()
    print(item_state_map)
    print(sat)
    print(solution)
    
    # TODO convert solution into "DFA" object which still needs to be defined
    return sat, solution
    

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
find_solution(glp_algorithm.obs_table, 
                   glp_algorithm.get_s_plus(), 
                   glp_algorithm.get_s_minus())
    




