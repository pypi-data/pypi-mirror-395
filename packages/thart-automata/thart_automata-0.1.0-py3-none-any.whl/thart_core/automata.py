import numpy as np
import itertools

def convert_custom(base):
    print(f"Calling Custom sequence conversion function for base {base}")
    custom_input = input(f"Enter custom sequence of digits (0 to {base-1}), comma-separated (e.g., 0,1,2,0,1,2): ")
    
    try:
        # Split by comma, strip whitespace, and convert to integers
        int_sequence = [int(x.strip()) for x in custom_input.split(',')]
    except ValueError:
        print("Invalid input format. Ensure only digits and commas are used.")
        return []
    
    # Validation step
    for digit in int_sequence:
        if not (0 <= digit < base):
            print(f"Error: Digit {digit} is outside the range 0 to {base-1}.")
            return []
            
    print(f"Successfully loaded custom sequence of length {len(int_sequence)}.")
    return int_sequence

def get_sequence_for_analysis(base):
    
    print("Processed sequence analysis")
    print("Please provide your sequence of pre-processed digits (0 to n-1).")
    converted_array = convert_custom(base) 
    return converted_array

class ThartAutomata:
    @staticmethod
    def _get_state_key(state_list):
        return "".join(map(str, state_list))
    
    
    def __init__(self, base, State_list, STATE_MAPPING):
        self.base = base
        self.State_list = State_list
        self.STATE_MAPPING = STATE_MAPPING
        
        self.stack = []
        self.full_log = []
        self.distinct_states_log = []
        self.log_state(is_recursive=False, is_initial=True)

    def push(self, x, is_recursive=False):
        
        if x in self.stack:
            self.stack.remove(x)
            new_val = (x + 1) % self.base 
            self.push(new_val, is_recursive=True)
        else:
            self.stack.append(x)

        if not is_recursive:
            self.log_state(is_recursive=False, is_initial=False)
            
    
    def _normalize_state(self, state):
        # Use self.base instead of the global base
        if len(state) == self.base and all(i in state for i in range(self.base)):
            return []
        return state.copy()
    def log_state(self, is_recursive, is_initial):
        current_state = self.stack.copy()
        normalized_state = self._normalize_state(current_state)

        if not is_recursive:
            self.full_log.append(normalized_state)

        if normalized_state not in self.distinct_states_log:
            self.distinct_states_log.append(normalized_state)
    def _calculate_frequency_matrix(self):
        log_length = len(self.full_log)
        if log_length < 2:
            return None, 0

        matrix_size = len(self.State_list)
        M = np.zeros((matrix_size, matrix_size))

        for k in range(log_length - 1):
            state_i = self.full_log[k]       
            state_j = self.full_log[k + 1]
            key_i = self._get_state_key(state_i)
            key_j = self._get_state_key(state_j)

            try:
                index_i = self.STATE_MAPPING[key_i]
                index_j = self.STATE_MAPPING[key_j]
            except KeyError:
                 return None, 0

            M[index_i, index_j] += 1
        return M, log_length - 1
        
    def export_matrix_to_r(self):
        M_freq, total_transitions = self._calculate_frequency_matrix()
        P = M_freq / total_transitions
        matrix_size = len(self.State_list)

        r_state_names = []
        for state in self.State_list:
            name_str = "[" + ", ".join(map(str, state)) + "]"
            r_state_names.append(name_str)
        r_matrix_str = f"P_matrix <- matrix(c("
        P_flat = P.T.flatten()
        r_matrix_str += ",".join([f"{x:.6f}" for x in P_flat])
        r_matrix_str += f"), nrow={matrix_size}, byrow=FALSE)"

        r_matrix_str += f"\nrownames(P_matrix) <- c(\"{'\", \"'.join(r_state_names)}\")"
        r_matrix_str += f"\ncolnames(P_matrix) <- c(\"{'\", \"'.join(r_state_names)}\")"
        r_matrix_str += "\n# Total transitions: " + str(total_transitions)
            
        return r_matrix_str
        
    def execute_custom_sequence(self, custom_arr):
        for num in custom_arr:
            self.push(num, is_recursive=False)
def setup_state_space():
    base = int(input("\n enter the base of the THART: "))

    digit_alphabet = list(range(base))
    State_list = []
    
    for i in range(base):
        for p_tuple in itertools.permutations(digit_alphabet, i):
            State_list.append(list(p_tuple))
    
    STATE_MAPPING = {}
    for index, state_list_item in enumerate(State_list):
        key_string = "".join(map(str, state_list_item))
        STATE_MAPPING[key_string] = index
        
    print(f"Base: {base} | Total States: {len(State_list)}")
    return base, State_list, STATE_MAPPING

def markov_analysis():
    base, State_list, STATE_MAPPING = setup_state_space() 

    
    converted_array = get_sequence_for_analysis(base) 
    
    if not converted_array:
        print("No valid sequence generated. Exiting.")
        return
        
    print("3. Executing Markov Chain simulation...")
    
    my_stack = ThartAutomata(base, State_list, STATE_MAPPING) 
    my_stack.execute_custom_sequence(converted_array)
    
    print(" -> Simulation complete.")
    print("\n--- R COMMAND ---")
    print(my_stack.export_matrix_to_r())

if __name__ == "__main__":
    markov_analysis()