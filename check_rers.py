from aalpy.base import SUL
from aalpy.base.SUL import CacheSUL
from rers_sul import RERSSUL
from aalpy.utils import load_automaton_from_file, make_input_complete
from aalpy.automata import MealyMachine
import os
import subprocess

M = load_automaton_from_file(os.path.join("rers2019/challenge_and_training_set_with_dotfiles", "m183.dot"), automaton_type='mealy')
alphabet = [x for x in M.get_input_alphabet() if x not in ["usr1_ai1_re2", "usr1_ai1_VoidReply","usr3_ai1_VoidReply","usr3_ai1_re1"]]

sul_T = CacheSUL(RERSSUL(for_T=True, is_prefix_closed=True, is_suffix_closed=False))
sul_B = CacheSUL(RERSSUL(for_T=False, is_prefix_closed=False, is_suffix_closed=True))

def compute_init():
    return M.initial_state

def compute_transition(s, a):
    return s.output_fun(a)

compute_init()
class Node:
    def __init__(self, data, prefix):
        self.data = data
        self.prefix = prefix
        self.round = 0
        self.transitions = {}

    def __eq__(self, other):
        return self.data == other.data and self.round == other.round

class DFS:
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def run(self):
        init_s = Node(compute_init(), tuple())
        visited = []
        stack = []
        stack.append(init_s)

        while len(stack):
            s = stack.pop()
            if s not in visited:
                visited.append(s)
            for e in self.alphabet:
                mealy_output = s.data.output_fun[e]
                new_s = Node(s.data.transitions[e], s.prefix + (e,))
                in_T = sul_T.query(new_s.prefix)[-1]
                in_B = sul_B.query(new_s.prefix)[-1]

                if mealy_output == "error" and in_T and (not in_B):
                    print(new_s.prefix)
                elif mealy_output != "error" and ((not in_T) or in_B):
                    print(new_s.prefix)

                if new_s not in visited:
                    stack.append(new_s)
                else:
                    new_s.round = 1
                    if new_s not in visited:
                        stack.append(new_s)


                if new_s.data is None:
                    continue
            print(len(visited), len(stack))

        return init_s, visited


dfs = DFS(alphabet)
init, visited = dfs.run()