import pandas as pd
import os


arithmetic =  ["m135", "m158", "m159", "m164", "m172", "m181", "m183", "m185", "m201", "m24", "m45", "m54", "m55", "m76", "m95"]
data_structures = ["m106", "m131", "m132", "m167", "m173", "m182", "m189", "m196", "m199", "m22", "m27", "m41"]

benchmarks = sorted(arithmetic, key=lambda x: int(x[1:])) + sorted(data_structures, key=lambda x: int(x[1:]))

dfs = []
t_type = "T3"
for benchmark in benchmarks:
    if os.path.isfile(f"/Users/tomyaacov/Downloads/results_24_3/results_{benchmark}_{t_type}_rpni.csv"):
        dfs.append(pd.read_csv(f"/Users/tomyaacov/Downloads/results_24_3/results_{benchmark}_{t_type}_rpni.csv"))
    else:
        dfs.append(pd.DataFrame([{"benchmark": benchmark, "L* time": -1}]))

pd.concat(dfs).to_csv(f'output/results_all_{t_type}_rpni.csv', index=False)

