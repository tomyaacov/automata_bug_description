from symbolic_dfa_t2 import SymbolicDFAT2
from data.counter_examples import counter_examples_dict
from data.alphabet import alphabet as alphabet_dict
from aalpy.oracles import RandomWMethodEqOracle
from aalpy.SULs import DfaSUL
from aalpy.learning_algs import run_Lstar

example = "m135"
dfa = SymbolicDFAT2(counter_examples_dict[example]["2"][0][1])
alphabet = alphabet_dict[example]
sul = DfaSUL(dfa)

eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=100, walk_len=50)

# start the L* and print the whole process in detail
learned_dfa = run_Lstar(alphabet, sul, eq_oracle, automaton_type='dfa',
                        cache_and_non_det_check=True, cex_processing=None, print_level=0)

print(learned_dfa)