from aalpy.base import SUL
from aalpy.base.Oracle import Oracle
from aalpy.oracles import RandomWMethodEqOracle

from utils import get_intersection_dfa, get_diff_dfa, are_dfa_equivalent, aalpy_to_automata_lib_format
from aalpy.automata import Dfa, DfaState
from automata.base.exceptions import EmptyLanguageException
import sys
class SystemDCOracle(Oracle):
    def __init__(self, alphabet: list, sul: SUL, M, traces):
        super().__init__(alphabet, sul)
        self.M = M
        self.traces = traces
        self.b_oracle = RandomWMethodEqOracle(alphabet, sul.system_sul, walks_per_state=200, walk_len=30)
        self.equivalence_queries = 0

    def find_cex(self, hypothesis):
        self.equivalence_queries += 1
        for label, trace in self.traces:
            if hypothesis.execute_sequence(hypothesis.initial_state, trace)[-1] != label:
                return trace

        T = self.moore_to_dfa(hypothesis, "+-")
        if not are_dfa_equivalent(T, self.M):
            A = aalpy_to_automata_lib_format(T)
            B = aalpy_to_automata_lib_format(self.M)
            C = A - B
            D = B - A
            try:
                C_k = C.minimum_word_length()
            except EmptyLanguageException:
                C_k = sys.maxsize
            try:
                D_k = D.minimum_word_length()
            except EmptyLanguageException:
                D_k = sys.maxsize
            if C_k < D_k:
                for word in C.words_of_length(C_k):
                    return self.str_to_word(word)
            else:
                for word in D.words_of_length(D_k):
                    return self.str_to_word(word)
            raise Exception("No counterexample found")
        else:
            B = self.moore_to_dfa(hypothesis, "+")
            cex = self.b_oracle.find_cex(B)
            if cex is not None:
                return cex
            return None

    def reset_hyp_and_sul(self, hypothesis):
        pass

    def moore_to_dfa(self, machine, accepting_output):
        d = {}
        for s in machine.states:
            d[s.state_id] = DfaState(s.state_id, is_accepting=s.output in accepting_output)
        for s in machine.states:
            for a, s2 in s.transitions.items():
                d[s.state_id].transitions[a] = d[s2.state_id]
        initial_state = d[machine.initial_state.state_id]
        return Dfa(initial_state, list(d.values()))

    def str_to_word(self, s):
        l = []
        while len(s) > 0:
            for a in self.alphabet:
                if s.startswith(a):
                    l.append(a)
                    s = s[len(a):]
        return tuple(l)
