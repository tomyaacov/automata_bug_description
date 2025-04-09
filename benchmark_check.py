from aalpy.utils import load_automaton_from_file, make_input_complete
from aalpy.automata import MealyMachine
import os
import subprocess



M = load_automaton_from_file(os.path.join("rers2019/challenge_and_training_set_with_dotfiles", "m183.dot"), automaton_type='mealy')
alphabet = M.get_input_alphabet()

def compute_init():
    #p = Popen("cd rers2019/IndReachabilityRers2019/arithmetic/m183;java m183_Reach", stdin=PIPE, stdout=PIPE)
    # p = Popen("cd rers2019/IndReachabilityRers2019/arithmetic/m183", stdin=PIPE, stdout=PIPE)
    process = subprocess.Popen(
        ['java', 'm183_Reach'],  # Name of the compiled Java class (without .class extension)
        stdin=subprocess.PIPE,  # Pipe to send input to the program
        stdout=subprocess.PIPE,  # Pipe to capture output
        stderr=subprocess.PIPE,  # Pipe to capture error (if any)
        text=True,  # Treat input and output as strings (instead of bytes)
        cwd="rers2019/IndReachabilityRers2019/arithmetic/m183"  # Set the working directory where the Java class is located
    )
    # Send input to the Java program and capture the output
    stdout, stderr = process.communicate("init" + "\n")
    state, new_hash = stdout.rstrip().split("\n")
    process.terminate()
    return state, new_hash

def compute_transition(s, a):
    #p = Popen("cd rers2019/IndReachabilityRers2019/arithmetic/m183;java m183_Reach", stdin=PIPE, stdout=PIPE)
    # p = Popen("cd rers2019/IndReachabilityRers2019/arithmetic/m183", stdin=PIPE, stdout=PIPE)
    process = subprocess.Popen(
        ['java', 'm183_Reach'],  # Name of the compiled Java class (without .class extension)
        stdin=subprocess.PIPE,  # Pipe to send input to the program
        stdout=subprocess.PIPE,  # Pipe to capture output
        stderr=subprocess.PIPE,  # Pipe to capture error (if any)
        text=True,  # Treat input and output as strings (instead of bytes)
        cwd="rers2019/IndReachabilityRers2019/arithmetic/m183"  # Set the working directory where the Java class is located
    )
    if s == "error":
        return "error", "error", "error", "Legal"
    # Send input to the Java program and capture the output
    stdout, stderr = process.communicate(s + "\n" + a)
    # Check if any error occurred
    # if stderr:
    #     if "IllegalStateException" in stderr:
    #         in_T, in_B = True, True
    #     elif "IllegalArgumentException" in stderr:
    #         in_T, in_B = False, False
    #     else:
    #         in_T, in_B = True, False
    # else:
    #     in_T, in_B = True, False
    # print(stdout)
    # print(stderr)
    output, new_state, new_hash, in_T = stdout.rstrip().split("\n")
    process.terminate()
    return output, new_state, new_hash, in_T

class Node:
    def __init__(self, data, hash):
        self.data = data
        self.hash = hash
        self.transitions = {}

    def __eq__(self, other):
        return self.hash == other.hash

class DFS:
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def run(self):
        init_s = Node(*compute_init())
        visited = []
        stack = []
        stack.append(init_s)

        while len(stack):
            s = stack.pop()
            if s not in visited:
                visited.append(s)
            for e in self.alphabet:
                output, new_state, new_hash, in_T = compute_transition(s.data, e)
                if output == "error":
                    new_s = Node("error", "error")
                else:
                    new_s = Node(new_state, new_hash)

                if new_s not in visited:
                    stack.append(new_s)

                if new_s.data is None:
                    continue
                s.transitions[e] = (new_s, output, in_T)
            print(len(visited), len(stack))

        return init_s, visited



# print(compute_transition("/7/166/4/190/238/g/e/e/226/e/15/g/-38/10/4/119/341/200/f/5/8/8/-53/10/g/11/e/384/e/g/-9/-69/-132/7/465/g/5/g/228/209/g/13/198/6/367/387/i/215/g/12/g/3/4/7/g/6/-52/g/3/f/-21/6/2/436/e/34/g/67/g/8/e/16/8/h/g",
#                          "ai1_ce1"))

dfs = DFS(alphabet)
init, visited = dfs.run()
