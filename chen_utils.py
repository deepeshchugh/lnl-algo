from constants import _Const
from observation_table import ObsTable
from three_dfa import TDFA
CONST = _Const()


def gen_3dfa(observation_table: ObsTable):
    state_count = 0
    row_string_to_state = {}
    word_to_state = {}
    state_to_words = {}
    final_states = set()
    dont_care_states = set()
    rejected_states = set()
    delta = {}
    main_table = observation_table.main_table
    alphabet = observation_table.alphabet
    for prefix in main_table:
        prefix_row_string = gen_row_string(main_table[prefix])
        if row_string_to_state.get(prefix_row_string, None) is None:
            state_count += 1
            row_string_to_state[prefix_row_string] = state_count
            word_to_state[prefix] = state_count
            state_to_words[state_count] = [prefix]
            if main_table[prefix][CONST.EMPTY] == CONST.POS:
                final_states.add(state_count)
            elif main_table[prefix][CONST.EMPTY] == CONST.NEG:
                rejected_states.add(state_count)
            elif main_table[prefix][CONST.EMPTY] == CONST.DONT_CARE:
                dont_care_states.add(state_count)
            else:
                raise RuntimeError("Unexpected state found:", main_table[prefix][CONST.EMPTY])
        else:
            row_state = row_string_to_state[prefix_row_string]
            word_to_state[prefix] = row_state
            state_to_words[row_state].append(prefix)

    
    for state in range(1, state_count + 1):
        delta[state] = {}
        transition_found_map = {}
        
        for word in state_to_words[state]:
            for letter in alphabet:
                if transition_found_map.get(letter, None) is None:
                    transition_found_map[letter] = False
                if not transition_found_map[letter]:
                    if word_to_state.get(word + letter, None) is not None:
                        delta[state][letter] = word_to_state[word + letter]
                        transition_found_map[letter] = True
        
        for letter in alphabet:
            if not transition_found_map[letter]:
                delta[state][letter] = state
    
    return TDFA(
        num_states=state_count,
        alphabet=alphabet,
        delta=delta,
        final_states=final_states,
        dont_care_states=dont_care_states,
        rejected_states=rejected_states,
        first_state=word_to_state[CONST.EMPTY]
    )
    
            




def gen_row_string(row):
    sorted_keys = sorted(row.keys())
    row_string = ""
    for key in sorted_keys:
        if row[key] == CONST.POS:
            row_string = row_string + 'p'
        elif row[key] == CONST.NEG:
            row_string = row_string + 'n'
        elif row[key] == CONST.DONT_CARE:
            row_string = row_string + 'd'
        else:
            raise RuntimeError("Invalid state found while generating row string:", row[key])
    return row_string




def row_exists_in_main_table(row, observation_table: ObsTable):
    for prefix in observation_table.prefix_set:
        if are_rows_equal(observation_table.main_table[prefix], row):
            return True
    return False

'''
Takes two rows as input,
Where each row (based on a prefix) is a dict (list)
mapping suffixes from the suffix set to a state

Returns a boolean based on the rows being equal or not
(Note: this is a straight equality check not a similarity check like glp)
'''
def are_rows_equal(row_1, row_2):
    difference = find_row_diff(row_1, row_2)
    if difference is None:
        return True
    return False

'''
Takes two rows as input,
Where each row (based on a prefix) is a dict (list)
mapping suffixes from the suffix set to a state

Returns:
None if the rows are equal
Else, the first suffix under which the two rows differ is returned
'''
def find_row_diff(row_1, row_2):
    for suffix in row_1:
        if row_1[suffix] == row_2[suffix]:
            continue
        else:
            return suffix
    return None


