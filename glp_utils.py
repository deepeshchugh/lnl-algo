from constants import _Const
CONST = _Const()

def similar_row_exists(row, observation_table):
    for prefix in observation_table.prefix_set:
        if are_rows_similar(observation_table.main_table[prefix], row):
            return True
    return False

def are_rows_similar(row_1, row_2):
    for suffix in row_1:
        if are_states_similar(row_1[suffix], row_2[suffix]):
            continue
        else:
            return False
    return True

def are_states_similar(state_1, state_2):
    if state_1 == CONST.DONT_CARE or state_2 == CONST.DONT_CARE:
        return True
    else:
        return state_1 == state_2


