'''
Contains constants used in the algorithm,
the presumption here is '$' is forbidden anywhere in alphabet etc
and is used as an escape character in constants
'''
def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class _Const(object):
    @constant
    def POS():
        return '+'
    @constant
    def NEG():
        return "-"
    @constant
    def DONT_CARE():
        return "?"
    @constant
    def LAMBDA():
        return "$lambda$"
    @constant
    def EMPTY():
        return ""
    @constant
    def MAX_DFA_SIZE():
        return 10