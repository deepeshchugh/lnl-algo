from constants import _Const
CONST = _Const()

'''
Creates an observation table row corresponding
to a given prefix (row definer) and 
the suffix set (col definers)
'''
def gen_obs_table_row(prefix, suffix_set):
    suffix_row = {}
    for suffix in suffix_set:
        suffix_row[suffix] = mem_query(prefix + suffix)
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
