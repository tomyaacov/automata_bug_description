from aalpy.base.SUL import CacheSUL
from rers_sul_s_t import RERSSULST
from aalpy.utils import load_automaton_from_file, make_input_complete
from system_dc_sul import SystemDCSUL
from data.counter_examples import counter_examples_dict

import os

from system_dc_sul_s_t import SystemDCSULST

# for benchmark in ["m135", "m158", "m159", "m164", "m172", "m181", "m183", "m185", "m201", "m24", "m45", "m54", "m55",
#                  "m76", "m95"] + ["m106", "m131", "m132", "m167", "m173", "m182", "m189", "m190", "m196", "m199", "m22", "m27", "m41",
#                    "m49", "m65"]:
#     sul = CacheSUL(RERSSUL(benchmark=benchmark, for_T=False, is_prefix_closed=False, is_suffix_closed=True))
#     print(benchmark, len(sul.sul.alphabet))

benchmark = "m185"
# l = [
# ['ai1_ce1', 'usr3_ai2_re1', 'usr4_ai2_VoidReply', 'usr2_ai3_re5', 'usr2_ai3_VoidReply', 'usr1_ai3_re40', 'assert']
# ]
# l = [
#     counter_examples_dict[benchmark]["3"][0][1]
# ]
l = [
['ai1_ce1', 'usr1_ai1_VoidReply', 'usr5_ai1_VoidReply', 'usr6_ai1_re1', 'usr5_ai1_re1', 'usr1_ai3_re39', 'usr1_ai3_VoidReply', 'usr4_ni1_ne1', 'usr4_ai1_re1', 'usr1_ai3_re37', 'usr7_ai1_VoidReply', 'usr1_ai1_VoidReply', 'usr1_ai1_VoidReply', 'usr1_ai3_VoidReply', 'usr5_ai1_VoidReply', 'assert', 'assert', 'assert', 'usr5_ai1_VoidReply']
]
# for word in l:
#     # if len(word) != 5:
#     #     continue
#     print(word)
#     sul = CacheSUL(RERSSULST(benchmark=benchmark,
#                            for_T=False,
#                            is_prefix_closed=False,
#                            is_suffix_closed=True,
#                            t_type='3',
#                              debug=True))
#     print(sul.query(tuple(word)))


# M = load_automaton_from_file(f'data/{benchmark}/T3.dot', automaton_type='dfa')
# make_input_complete(M, missing_transition_go_to="sink_state")

system_sul = CacheSUL(RERSSULST(benchmark=benchmark, t_type='3', for_T=False, is_prefix_closed=False, is_suffix_closed=False, debug=True))
# alphabet = system_sul.sul.alphabet

for word in l:
    # for i in range(len(word)):
    #     print(system_sul.query(tuple(word[:i])))
    try:
        print(system_sul.query(tuple(word)))
    except ValueError as e:
        print("error", e.args[0])

# lst = ["usr3_ai1_re2","usr3_ai1_re1","usr7_ai3_re16","usr1_ni1_ne1","usr5_ai1_re1","usr5_ai2_VoidReply","usr7_ai3_re28","usr7_ai3_re34","usr7_ai3_re11","usr5_ai1_re2","usr7_ai3_re30","usr7_ai3_re42","usr7_ai3_re25","usr7_ai3_re26","usr7_ai3_re27","usr7_ai3_re46","usr7_ai3_re21","usr7_ai3_re23","usr5_ai1_VoidReply","usr5_ai1_re4","usr5_ai1_re7","usr5_ai1_re6","usr1_ai1_VoidReply","usr7_ai3_re29","usr7_ai3_re38","usr1_ai1_re1","usr7_ai3_re15","ai1_ce3","usr1_ai1_re2","ai1_ce4","usr2_ai1_re2","usr7_ai3_re24","usr2_ai1_re1","usr2_ni1_ne1","usr3_ni1_ne1","usr6_ai1_VoidReply","ai1_ce1","usr2_ai1_VoidReply","usr8_ai1_VoidReply","usr7_ai3_VoidReply","usr7_ai3_re19","usr3_ai1_VoidReply","usr7_ai3_re17","usr7_ai3_re51","ai1_ce2","usr9_ai1_VoidReply","usr7_ai3_re18","usr7_ai1_VoidReply","usr7_ai3_re33","usr7_ai3_re14","usr7_ai3_re31","usr7_ai3_re45","usr7_ai3_re37","usr7_ai3_re10","usr7_ai3_re35","usr7_ai3_re12","usr5_ai1_re5","usr7_ai3_re9","usr4_ai1_re1","usr7_ai3_re32","usr7_ai3_re5","usr7_ai3_re4","usr7_ai3_re7","usr7_ai3_re6","usr7_ai3_re1","usr7_ai3_re48","usr7_ai3_re2"]
# for c in lst:
#     for c1 in lst:
#         for c2 in lst:
#             print(system_sul.query(tuple(['ai1_ce1', c, c1, c2])))




