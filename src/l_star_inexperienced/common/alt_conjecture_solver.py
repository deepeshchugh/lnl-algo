'''
This module responsible for encoding a given conjecture into
its given cnf form, matching the glp constraints and attempting to 
find a solution using naive iteration 
(ignoring binary search recommendation for now)
'''

from .observation_table import ObsTable
from .constants import _Const
from ..dfa.dfa import DFA

import pycosat

CONST = _Const()


'''
Primary external function of this module
i/p: Observation Table, S Plus Set, S Minus Set
o/p: Minimal DFA Object matching constraint
'''
def alt_find_solution(obsTable: ObsTable, s_plus: set, s_minus: set, max_dfa_size = None, show_logs = False):
    if max_dfa_size is None:
        max_dfa_size = CONST.MAX_DFA_SIZE

    n = 1
    
    print("In alternate solver!")
    while n <= max_dfa_size:
        if show_logs:
            print("n: ", n)
        foundDFA, proposed_dfa = alt_find_dfa_with_size(obsTable=obsTable, 
                        s_plus=s_plus, s_minus=s_minus, 
                        num_states=n)
        if foundDFA:
            if show_logs:
                print("Found at n = ", n)
            return proposed_dfa
        n+=1
    if n > max_dfa_size:
        if show_logs:
            print("Error, not able to find DFA within given constraints")
        return None

'''
One iteration of sat solver
takes i/p: obsTable, s plus set, s minus set, number of states
o/p: foundDFA: boolean, DFA 
Adds clauses according to the four constraints provided in glp sat based approach
'''
def alt_find_dfa_with_size(obsTable: ObsTable, s_plus: set, s_minus: set, num_states):
    alphabet = obsTable.alphabet

    combined_words = set()
    for item in s_plus:
        combined_words.update(alt_get_prefix_set(item))
    for item in s_minus:
        combined_words.update(alt_get_prefix_set(item))
    
    item_state_map = {}
    item_increment = 0
    for item in combined_words:
        state_list = []
        for i in range(1, num_states+1):
            state_list.append(item_increment + i)
        item_state_map[item] = state_list
        item_increment += num_states
    
    all_clauses = []
    # Clause 1
    for item in combined_words:
        clause_list = []
        for i in range(0, num_states):
            clause_list.append(item_state_map[item][i])
        all_clauses.append(clause_list)
    
    # Clause 2
    for item in combined_words:
        for i in range(0, num_states-1):
            for j in range(i+1, num_states):
                all_clauses.append([-1 * item_state_map[item][i], 
                              -1 * item_state_map[item][j]])
    
    # Clause 3
    for item_1 in combined_words:
        for item_2 in combined_words:
            if item_1 == item_2:
                continue
            for letter in alphabet:
                if item_1 + letter in combined_words:
                    if item_2 + letter in combined_words:
                        for i in range(0, num_states):
                            for j in range(0, num_states):
                                all_clauses.append([-1 * item_state_map[item_1][i], 
                                              -1 * item_state_map[item_2][i], 
                                              -1 * item_state_map[item_1 + letter][j], 
                                              item_state_map[item_2 + letter][j]])
                                all_clauses.append([-1 * item_state_map[item_1][i], 
                                              -1 * item_state_map[item_2][i], 
                                              item_state_map[item_1 + letter][j], 
                                              -1 * item_state_map[item_2 + letter][j]])

    # Clause 4
    for item_1 in s_plus:
        for item_2 in s_minus:
            for i in range(0, num_states):
                all_clauses.append([-1 * item_state_map[item_1][i], -1 * item_state_map[item_2][i]])
    
    solution = pycosat.solve(all_clauses)
    solution_found = False
    proposed_dfa = None
    if type(solution) is list:
        converted_solution = []
        converted_solution.append(None)
        for state_representation in solution:
            if state_representation > 0:
                converted_solution.append(True)
            else:
                converted_solution.append(False)
        proposed_dfa = alt_generate_dfa(num_states, obsTable=obsTable, s_plus=s_plus,
                 item_state_map=item_state_map, solution=tuple(converted_solution))
        solution_found = True

    return solution_found, proposed_dfa

def alt_generate_dfa(num_states, obsTable: ObsTable, s_plus, item_state_map, solution):
    word_to_state_map = {}
    state_to_word_map = {}
    for i in range(1, num_states+1):
        state_to_word_map[i] = []

    for word in item_state_map:
        for i in range(0, num_states):
            if solution[item_state_map[word][i]]:
                word_to_state_map[word] = i+1
                state_to_word_map[i+1].append(word)

    delta = {}
    for i in range(1, num_states+1):
        delta[i] = {}
        for letter in obsTable.alphabet:
            transition_found = False
            for word in state_to_word_map[i]:
                if (word + letter) in word_to_state_map:
                    delta[i][letter] = word_to_state_map[word + letter]
                    transition_found = True
                    break
            if not transition_found:
                delta[i][letter] = i
            

    final_states = set()
    first_state = None
    for i in range(1, num_states+1):
        for word in state_to_word_map[i]:
            if word in s_plus:
                final_states.add(i)
                break
        if CONST.EMPTY in state_to_word_map[i]:
            first_state = i

    return DFA(
        num_states=num_states,
        alphabet=obsTable.alphabet,
        delta=delta,
        final_states=final_states,
        first_state=first_state
    )

def alt_get_prefix_set(word):
        word_array = [""]
        prefix_set = set([""])
        for char in word:
            word_array.append(char)
            prefix_set.add(''.join(word_array))
        return prefix_set



