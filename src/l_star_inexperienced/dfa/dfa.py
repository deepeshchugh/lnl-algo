from cgi import test
from visual_automata.fa.dfa import VisualDFA

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
    
    # Experimental
    def visualize(self):
        state_to_viz_map = {}
        states = []
        transitions = {}
        for state in range(1, self.num_states + 1):
            state_to_viz_map[state] = 'q' + str(state)
            states.append(state_to_viz_map[state])
        
        for state in range(1, self.num_states + 1):
            transitions[state_to_viz_map[state]] = {}
            for letter in self.alphabet:
                transitions[state_to_viz_map[state]][letter] = state_to_viz_map[self.delta[state][letter]]

        initial_state = state_to_viz_map[self.first_state]
        final_states = []
        for final_state in self.final_states:
            final_states.append(state_to_viz_map[final_state])
        
        visual_dfa = VisualDFA(
        states=set(states),
        input_symbols=set(self.alphabet),
        transitions=transitions,
        initial_state=initial_state,
        final_states=set(final_states),
        )

        visual_dfa.show_diagram(view=True)

if __name__ == "__main__":
    # Unit testing!
    delta = {}
    delta[1] = {'a':2,'b':3}
    delta[2] = {'a':1,'b':4}
    delta[3] = {'a':4,'b':1}
    delta[4] = {'a':3,'b':2}

    test_dfa = DFA(
        num_states=4,
        alphabet=['a', 'b'],
        delta=delta,
        final_states=set([1]),
        first_state=1
    )
    
    test_dfa.print_parameters()
    failedTest = False

    if not test_dfa.is_state_final(1):
        print("Accepting state not verified")
        failedTest = True

    if not test_dfa.is_word_accepted(""):
        print("Valid word rejected")
        failedTest = True

    returnedState =  test_dfa.get_state_for_word("aabbaa")
    if not (returnedState == 1):
        print("Expected state 1, got invalid state: ", returnedState )
        failedTest = True

    for i in range(2,5):
        if test_dfa.is_state_final(i):
            print("Rejecting state treated as Final :", i)
            failedTest = True

    if test_dfa.is_word_accepted("aba"):
        print("invalid word accepted")
        failedTest = True

    if not failedTest:
        print("All unit tests passed successfully")
    else:
        print("Atleast one unit test has failed, please check previous logs for details.")

