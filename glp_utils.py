from constants import _Const
CONST = _Const()


def similar_row_exists_in_main_table(row, observation_table):
    for prefix in observation_table.prefix_set:
        if are_rows_similar(observation_table.main_table[prefix], row):
            return True
    return False

'''
Takes two rows as input,
Where each row (based on a prefix) is a dict (list)
mapping suffixes from the suffix set to a state

Returns a boolean based on the rows being similar or not
(two rows are similar if a row which behaves the 
same as both rows exists)
'''
def are_rows_similar(row_1, row_2):
    difference = find_row_diff(row_1, row_2)
    if difference is None:
        return True
    return False

'''
Takes two rows as input,
Where each row (based on a prefix) is a dict (list)
mapping suffixes from the suffix set to a state

Returns:
None if the rows are similar (i.e. a row which behaves the 
same as both rows exists)
Else, the first suffix under which the two rows differ is returned
'''
def find_row_diff(row_1, row_2):
    for suffix in row_1:
        if are_states_similar(row_1[suffix], row_2[suffix]):
            continue
        else:
            return suffix
    return None

'''
Basis for all comparison in glp 
If either state is "Dont care", the states are similar
else we do a formal comparison
'''
def are_states_similar(state_1, state_2):
    if state_1 == CONST.DONT_CARE or state_2 == CONST.DONT_CARE:
        return True
    else:
        return state_1 == state_2


