class DFA:
    
    '''
    Initiates DFA with 
    number of states, transition function delta, alphabet, 
    final states, & initial state
    Presumes states are 1 indexed
    '''
    def __init__(self, num_states, alphabet, delta, final_states, first_state):
        self.num_states = num_states
        self.alphabet = alphabet
        self.delta = delta
        self.final_states = final_states
        self.first_state = first_state
    
    def print_parameters(self):
        print("Number of states: ", self.num_states)
        print("Alphabet: ", self.alphabet)
        print("First State: ", self.first_state)
        print("Final States: ", self.final_states)
        print("Delta Function: ", self.delta)
    
    def is_word_accepted(self, word):
        return self.is_state_final(self.get_state_for_word(word))

    def get_state_for_word(self, word):
        current_state = self.first_state
        for letter in word:
            current_state = self.delta[current_state][letter]
        return current_state
    
    def is_state_final(self, state):
        return (state in self.final_states)