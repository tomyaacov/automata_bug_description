from aalpy.base.SUL import CacheSUL
from rers_sul import RERSSUL


benchmarks = ["m135", "m158", "m159", "m164", "m172", "m181", "m183", "m185", "m201", "m24", "m45", "m54", "m55",
                 "m76", "m95"] + ["m106", "m131", "m132", "m167", "m173", "m182", "m189", "m190", "m196", "m199", "m22", "m27", "m41",
                   "m49", "m65"]

for benchmark in benchmarks:
    print(benchmark)
    sul = CacheSUL(RERSSUL(benchmark=benchmark, for_T=False, is_prefix_closed=False, is_suffix_closed=True))

    if benchmark in ["m135", "m158", "m159", "m164", "m172", "m181", "m183", "m185", "m201", "m24", "m45", "m54", "m55",
                     "m76", "m95"]:
        dir = "rers2019/IndReachabilityRers2019/arithmetic/" + benchmark
    elif benchmark in ["m106", "m131", "m132", "m167", "m173", "m182", "m189", "m190", "m196", "m199", "m22", "m27",
                       "m41",
                       "m49", "m65"]:
        dir = "rers2019/IndReachabilityRers2019/data-structures/" + benchmark
    else:
        raise ValueError("Unknown benchmark")

    with open(dir + "/" + benchmark + ".traces", "r") as f:
        first_line = True
        c = 0
        for line in f:
            if first_line:
                first_line = False
                continue
            try:
                if any(sul.query(tuple(line.strip().split()[2:]))):
                    print(line.strip().split()[2:])
            except Exception as e:
                print(e)
                break
