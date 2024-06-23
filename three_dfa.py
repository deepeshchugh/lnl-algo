from dfa import DFA

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