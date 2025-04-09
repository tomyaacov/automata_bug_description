from aalpy.base import SUL
from aalpy.base.SUL import CacheSUL
from aalpy.utils import load_automaton_from_file, make_input_complete, save_automaton_to_file
from aalpy.automata import MealyMachine
import os
import subprocess
import argparse
from data.alphabet import alphabet



class RERSSUL(SUL):
    def __init__(self, benchmark, for_T=True, is_prefix_closed=True, is_suffix_closed=False, T=None, debug=False):
        super().__init__()
        self.state = None
        self.hash = None
        self.already_rejected = False
        self.already_accepted = False
        self.for_T = for_T
        self.is_prefix_closed = is_prefix_closed  # for T
        self.is_suffix_closed = is_suffix_closed  # for B
        self.memory = {}
        self.T = T
        self.benchmark = benchmark
        if benchmark in ["m135", "m158",  "m159", "m164", "m172", "m181", "m183", "m185", "m201", "m24", "m45", "m54", "m55", "m76", "m95"]:
            self.cwd = "rers2019/IndReachabilityRers2019/arithmetic/" + benchmark
        elif benchmark in ["m106", "m131", "m132", "m167", "m173", "m182", "m189", "m190", "m196", "m199", "m22", "m27", "m41", "m49", "m65"]:
            self.cwd = "rers2019/IndReachabilityRers2019/data-structures/" + benchmark
        else:
            raise ValueError("Unknown benchmark")
        # with open(f"{self.cwd}/{self.benchmark}_Reach.java") as f:
        #     data = f.read()
        #     a = data.find("String[] inputs = {")
        #     l_str = data[a + len("String[] inputs = {"):data.find("}", a)]
        #     self.alphabet = l_str.replace('"', "").split(",")
        self.alphabet = alphabet[benchmark]
        # if len(self.alphabet) == 0:
        #     raise ValueError("Empty alphabet")
        self.debug = debug
    def compute_init(self):
        process = subprocess.Popen(
            ['java', self.benchmark + '_Reach'],  # Name of the compiled Java class (without .class extension)
            stdin=subprocess.PIPE,  # Pipe to send input to the program
            stdout=subprocess.PIPE,  # Pipe to capture output
            stderr=subprocess.PIPE,  # Pipe to capture error (if any)
            text=True,  # Treat input and output as strings (instead of bytes)
            cwd=self.cwd
            # Set the working directory where the Java class is located
        )
        # Send input to the Java program and capture the output
        stdout, stderr = process.communicate("init" + "\n")
        state, new_hash = stdout.rstrip().split("\n")
        process.terminate()
        return state, new_hash

    def compute_transition(self, s, a):
        process = subprocess.Popen(
            ['java', self.benchmark + '_Reach'],  # Name of the compiled Java class (without .class extension)
            stdin=subprocess.PIPE,  # Pipe to send input to the program
            stdout=subprocess.PIPE,  # Pipe to capture output
            stderr=subprocess.PIPE,  # Pipe to capture error (if any)
            text=True,  # Treat input and output as strings (instead of bytes)
            cwd=self.cwd
            # Set the working directory where the Java class is located
        )
        if s == "error":
            return "error", "error", "error", "Legal"
        # Send input to the Java program and capture the output
        stdout, stderr = process.communicate(s + "\n" + a)
        # print(stdout)
        # print(stderr)
        outputs = stdout.rstrip().split("\n")
        if len(outputs) == 4:
            output, new_state, new_hash, in_T = outputs
        else:
            output = ""
            new_state, new_hash, in_T = stdout.rstrip().split("\n")
        process.terminate()
        return output, new_state, new_hash, in_T

    def query(self, word: tuple) -> list:
        self.pre()
        if len(word) == 0:
            if self.for_T:
                out = [True]
            else:
                out = [False]
        else:
            out = [self.step(letter) for letter in word]
        self.post()
        return out

    def pre(self):
        self.state, self.hash = self.compute_init()
        if self.for_T:
            self.already_rejected = False
            self.already_accepted = True
        else:
            self.already_rejected = True
            self.already_accepted = False
            if self.T is not None:
                self.T.reset_to_initial()
    def post(self):
        self.state = None
        self.hash = None
        self.already_rejected = False
        self.already_accepted = False
        if self.T is not None:
            self.T.reset_to_initial()

    def step(self, letter):
        if self.for_T:
            if self.is_prefix_closed and self.already_rejected:
                return False
        else:
            if self.is_suffix_closed and self.already_accepted:
                return True
        if (self.state, letter) not in self.memory:
            output, new_state, new_hash, in_T = self.compute_transition(self.state, letter)
            self.memory[(self.state, letter)] = (output, new_state, new_hash, in_T)
        else:
            output, new_state, new_hash, in_T = self.memory[(self.state, letter)]
        self.state = new_state
        self.hash = new_hash
        if self.for_T:
            if in_T != "Legal":
                self.already_rejected = True
            return in_T == "Legal"
        else:
            # print(in_T)
            if self.T is not None:
                t_label = self.T.step(letter)
                if self.debug:
                    print(t_label)
            # if (not self.already_accepted) and output == "error":  # TODO: fix bug after
            #     self.already_accepted = True
            #     return self.already_accepted
            if output == "error":
                self.already_accepted = True
            if self.debug:
                return self.already_accepted # and t_label  # maybe we need to change this to "error" == output
            else:
                return self.already_accepted and t_label  # maybe we need to change this to "error" == output


# sul = CacheSUL(RERSSUL(for_T=False, is_prefix_closed=False, is_suffix_closed=True))
# print(sul.query(("ai1_ce1", "ai1_ce1")))



from aalpy.oracles import BreadthFirstExplorationEqOracle
from aalpy.oracles.WMethodEqOracle import WMethodEqOracle, RandomWMethodEqOracle
from aalpy.base.Oracle import Oracle
from aalpy.learning_algs import run_Lstar
from itertools import product
from random import shuffle

class NewBreadthFirstExplorationEqOracle(BreadthFirstExplorationEqOracle):
    def __init__(self, alphabet, sul, depth):
        Oracle.__init__(self, alphabet, sul)
        self.depth = depth
        self.queue = []

        # generate all test-cases
        for seq in product(self.alphabet, repeat=self.depth):
            input_seq = tuple(seq)
            self.queue.append(input_seq)

        shuffle(self.queue)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--benchmark', '-B', type=str, default="m183")
    parser.add_argument('--discover', '-D', type=str, default="B")
    parser.add_argument('--walks_per_state', '-W', type=int, default=100)
    parser.add_argument('--walk_len', '-L', type=int, default=50)
    args = parser.parse_args()

    if args.discover == "T":
        sul = CacheSUL(RERSSUL(benchmark=args.benchmark, for_T=True, is_prefix_closed=True, is_suffix_closed=False))
        #sul = CacheSUL(RERSSUL(benchmark=args.benchmark, for_T=True, is_prefix_closed=False, is_suffix_closed=False)) # not prefix closed
    else:
        sul = CacheSUL(RERSSUL(benchmark=args.benchmark, for_T=False, is_prefix_closed=False, is_suffix_closed=False))

    alphabet = sul.sul.alphabet
    # print(len(alphabet))
    # print(sul.query(('ai2_ce3', 'usr2_ai2_VoidReply', 'usr3_ai1_re1', 'usr1_ni1_ne1', 'ai3_ce2')))


    # eq_oracle = NewBreadthFirstExplorationEqOracle(alphabet, sul, depth=4)
    # eq_oracle = WMethodEqOracle(alphabet, sul, max_number_of_states=len(sul.sul.A.states)*2)
    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=args.walks_per_state, walk_len=args.walk_len)

    learned_dfa = run_Lstar(alphabet, sul, eq_oracle, automaton_type='dfa', cache_and_non_det_check=True,
                            cex_processing=None, print_level=3)

    os.makedirs(f'output/{args.benchmark}', exist_ok=True)
    save_automaton_to_file(learned_dfa, f'output/{args.benchmark}/{args.discover}.dot', 'dot')
