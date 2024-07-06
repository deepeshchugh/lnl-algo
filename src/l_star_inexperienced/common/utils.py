'''
    For functions that may be used for generic operations
'''

'''
    Reduces list of lists to set equivalent (removes duplicates)
    Note: (order in list item matters)

    Input: list of any kind
    Output: deduped version of list in list of list format 
'''
def only_uniques(input_list):
    if isinstance(input_list, list):
        temp_set = set(tuple(i) for i in input_list)
        return list(list(i) for i in temp_set)
    else:
        raise TypeError("Expected list of lists received: " + input_list)


if __name__ == "__main__":
    dupe_list = [
        [1,2,3],
        [2,3,4],
        [1,2,3,4],
        [3,1,2,4],
        [1,2,3]
    ]
    print(dupe_list)
    print(only_uniques(dupe_list))