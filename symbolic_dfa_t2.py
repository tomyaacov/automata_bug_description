from aalpy.automata import Dfa, DfaState
from algorithm import learn
from fa_learner import FALearner
from dfa3_encoder import DFA3Encoder
from rpni_learner import RPNILearner
from aalpy.utils import make_input_complete, load_automaton_from_file
from rc_lstar import run_Lstar
import time
from system_dc_sul_s_t import SystemDCSULST
from system_dc_oracle_s_t import SystemDCOracleST
from complete_dfa_oracle import CompleteDFAOracle
from copy import deepcopy
from aalpy.base.SUL import CacheSUL
from rers_sul_s_t import RERSSULST
from data.counter_examples import counter_examples_dict
from multiprocessing import Process, Queue

class SymbolicDFAT2(Dfa):
    def __init__(self, counter_example):
        self.counter_example = counter_example
        self.current_gen = self._gen()
        self.current_gen.send(None)
        self.initial_state = DfaState("")
        self.initial_state.is_accepting = False
        self.states = []

    def step(self, letter):
        o = self.current_gen.send(letter)
        return o

    def reset_to_initial(self):
        self.current_gen = self._gen()
        self.current_gen.send(None)

    def _gen(self):
        seq = []
        while True:
            a = yield sorted(seq) == sorted(self.counter_example)
            if a in self.counter_example:
                if seq.count(a) < self.counter_example.count(a):
                    seq.append(a)


if __name__ == '__main__':
    counter_example = ['ai1_ce2', 'usr2_ai2_re5', 'usr2_ai4_re8', 'ai1_ce7', 'usr5_ai1_re1', 'usr3_ai1_VoidReply', 'usr2_ai4_re12']
    dfa = SymbolicDFAT2(counter_example)
    system_sul = CacheSUL(
        RERSSULST(benchmark="m199", t_type="2", for_T=False, is_prefix_closed=False, is_suffix_closed=False))
    alphabet = system_sul.sul.alphabet
    sul = SystemDCSULST(dfa, system_sul)
    sul.query(tuple(counter_example))

