'''
For functions that may be used for generic operations
'''

'''
Reduces list of lists to set equivalent (removes duplicates)

Input: list of any kind
Output: deduped version of list in list of list format
'''
def only_uniques(input_list):
    if isinstance(input_list(), list):
        temp_set = set(tuple(i) for i in input_list)
        return list(list(i) for i in temp_set)
    else:
        raise TypeError("Expected list of lists received: " + input_list)
