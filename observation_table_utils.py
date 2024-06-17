from constants import _Const
from teacher import Teacher
CONST = _Const()

'''
Creates an observation table row corresponding
to a given prefix (row definer), 
the suffix set (col definers),
and the corresponding teacher (for membership queries)
'''
def gen_obs_table_row(prefix, suffix_set, teacher: Teacher):
    suffix_row = {}
    for suffix in suffix_set:
        suffix_row[suffix] = teacher.membership_query(prefix + suffix)
    return suffix_row

# TODO dummy function replace with teacher functionality
def mem_query(string):
    if string == '':
        return CONST.POS
    if string == '00':
        return CONST.POS
    if string == '01':
        return CONST.DONT_CARE
    return CONST.NEG

# TODO dummy function replace with teacher functionality
def other_mem_query(string):
    zero_count = 0
    one_count = 0
    if string == '':
        return CONST.POS
    for char in string:
        if char is '0':
            zero_count += 1
        elif char is '1':
            one_count += 1
    if zero_count%2 == 0:
        return CONST.POS
    # elif string == '1000':
    #     return CONST.POS
    # elif one_count%2 == 0:
    #     return CONST.DONT_CARE
    else:
        return CONST.NEG