from cgi import test
from .dfa import DFA

class TDFA:
    
    '''
    Initiates 3DFA with 
    number of states, transition function delta, alphabet, 
    final states, don't care states, rejected_states & initial state
    Presumes states are 1 indexed
    '''
    def __init__(self, num_states, alphabet, delta, 
                 final_states: set, dont_care_states: set, rejected_states: set, 
                 first_state):
        self.num_states = num_states
        self.alphabet = alphabet
        self.delta = delta
        self.final_states = final_states
        self.dont_care_states = dont_care_states
        self.rejected_states = rejected_states
        if len(final_states) + len(dont_care_states) + len(rejected_states) != num_states:
            raise RuntimeError("State Count mismatch, array: ", 
                               [num_states, len(final_states), len(dont_care_states), len(rejected_states)])
        self.first_state = first_state
    
    def print_parameters(self):
        print("Number of states: ", self.num_states)
        print("Alphabet: ", self.alphabet)
        print("First State: ", self.first_state)
        print("Final States: ", self.final_states)
        print("Dont Care States: ", self.dont_care_states)
        print("Rejected States: ", self.rejected_states)
        print("Delta Function: ", self.delta)
    
    def is_word_accepted(self, word):
        return self.is_state_final(self.get_state_for_word(word))
    
    def is_word_dont_care(self, word):
        return self.is_state_dont_care(self.get_state_for_word(word))
    
    def is_word_rejected(self, word):
        return self.is_state_rejected(self.get_state_for_word(word))

    def get_state_for_word(self, word):
        current_state = self.first_state
        for letter in word:
            current_state = self.delta[current_state][letter]
        return current_state
    
    def is_state_final(self, state):
        return (state in self.final_states)
    
    def is_state_dont_care(self, state):
        return (state in self.dont_care_states)
    
    def is_state_rejected(self, state):
        return (state in self.rejected_states)
    
    def get_c_plus(self):
        return DFA(
            num_states=self.num_states,
            alphabet=self.alphabet,
            delta=self.delta,
            final_states=self.final_states.union(self.dont_care_states),
            first_state=self.first_state
        )
    
    def get_c_minus(self):
        return DFA(
            num_states=self.num_states,
            alphabet=self.alphabet,
            delta=self.delta,
            final_states=self.final_states,
            first_state=self.first_state
        )
    

if __name__ == "__main__":
    # Unit Testing!
    delta = {}
    delta[1] = {'a':2,'b':3}
    delta[2] = {'a':1,'b':4}
    delta[3] = {'a':4,'b':1}
    delta[4] = {'a':3,'b':2}

    test_tdfa = TDFA(
        num_states=4,
        alphabet=['a', 'b'],
        delta=delta,
        final_states=set([1]),
        dont_care_states=set([2,3]),
        rejected_states=set([4]),
        first_state=1
    )
    test_tdfa.print_parameters()
    failedTest = False
    test_c_minus = test_tdfa.get_c_minus()
    if (test_c_minus.delta != delta  or 
        test_c_minus.num_states != test_tdfa.num_states or
        len(test_c_minus.final_states.symmetric_difference(set([1]))) > 0 or
        test_c_minus.first_state != 1 or
        test_c_minus.alphabet != test_tdfa.alphabet):
        
        test_c_minus.print_parameters()
        print("Unexpected behaviour of C minus")
        failedTest = True

    test_c_plus = test_tdfa.get_c_plus()
    if (test_c_plus.delta != delta  or 
        test_c_plus.num_states != test_tdfa.num_states or
        len(test_c_plus.final_states.symmetric_difference(set([1,2,3]))) > 0 or
        test_c_plus.first_state != 1 or
        test_c_plus.alphabet != test_tdfa.alphabet):
        
        test_c_plus.print_parameters()
        print("Unexpected behaviour of C plus")
        failedTest = True
    
    if not test_tdfa.is_state_final(1):
        print("Accepting state not verified")
        failedTest = True
    
    if test_tdfa.is_state_final(2):
        print("Don't care state treated as accepting")
        failedTest = True
    
    if  test_tdfa.is_state_final(4):
        print("Rejected state treated as accepting")
        failedTest = True

    if not test_tdfa.is_word_accepted(""):
        print("Valid word not accepted")
        failedTest = True
    
    if test_tdfa.is_word_accepted("a"):
        print("Don't care word accepted")
        failedTest = True
    
    if test_tdfa.is_word_accepted("ab"):
        print("Rejected word accepted")
        failedTest = True


    if not test_tdfa.is_state_dont_care(2):
        print("Dont Care State not verified")
        failedTest = True
    
    if  test_tdfa.is_state_dont_care(4):
        print("Rejecting State labelled as don't care")
        failedTest = True

    if  test_tdfa.is_state_dont_care(1):
        print("Accepting State labelled as don't care")
        failedTest = True

    if test_tdfa.is_word_dont_care(""):
        print("Valid word treated as Dont care")
        failedTest = True
    
    if not test_tdfa.is_word_dont_care("a"):
        print("Don't care word not treated as one")
        failedTest = True
    
    if test_tdfa.is_word_dont_care("ab"):
        print("Rejected word treated as don't care")
        failedTest = True

    if not test_tdfa.is_state_rejected(4):
        print("Rejecting State not verified")
        failedTest = True
    
    if  test_tdfa.is_state_rejected(2):
        print("don't care state labelled as rejecting")
        failedTest = True

    if  test_tdfa.is_state_rejected(1):
        print("Accepting State labelled as rejecting")
        failedTest = True

    if not test_tdfa.is_word_rejected("ab"):
        print("Rejected word not treated as one")
        failedTest = True
    
    if test_tdfa.is_word_rejected(""):
        print("Accepted word treated as rejected")
        failedTest = True
    
    if test_tdfa.is_word_rejected("a"):
        print("Don't care word treated as rejected")
        failedTest = True

    returnedState =  test_tdfa.get_state_for_word("aabbaa")
    if not (returnedState == 1):
        print("Expected state 1, got invalid state: ", returnedState )
        failedTest = True

    if not failedTest:
        print("All unit tests passed successfully")
    else:
        print("Atleast one unit test has failed, please check previous logs for details.")
