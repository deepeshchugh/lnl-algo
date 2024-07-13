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