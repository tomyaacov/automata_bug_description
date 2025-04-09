import argparse
from main_single import main_single
import pandas as pd
from stopit import SignalTimeout as Timeout
import random

parser = argparse.ArgumentParser()
parser.add_argument('--benchmark', '-B', type=str, default="m158")
parser.add_argument('--method', '-M', type=str, default="rpni")
# parser.add_argument('--description_type', '-D', type=str, default="FE")
parser.add_argument('--t_type', '-T', type=str, default="1")
# parser.add_argument('--early_detection', '-E', action='store_true')
args = parser.parse_args()

random.seed(0)

if args.benchmark == "all":
    benchmarks = ["m158", "m172", "m183", "m24", "m45", "m54", "m76", "m95", "m199", "m27", "m164", "m159", "m55",
                  "m135", "m185", "m181", "m201", "m196", "m173", "m41", "m106", "m22", "m167", "m189", "m182", "m131",
                  "m132"]
else:
    benchmarks = [args.benchmark]

results_list = []
for benchmark in benchmarks:
    print("*****************", benchmark, "*****************")
    with Timeout(60.0*60*10) as timeout_ctx:
        results = main_single(benchmark, args.t_type, args.method, None, None)
    if timeout_ctx.state == timeout_ctx.TIMED_OUT:
        results = {"benchmark": benchmark, "L* time": 0}
    results_list.append(results)

df = pd.DataFrame(results_list)
import os
if not os.path.exists("output"):
    os.makedirs("output")
df.to_csv(f'output/results_{args.benchmark}_T{args.t_type}_{args.method}.csv', index=False)




