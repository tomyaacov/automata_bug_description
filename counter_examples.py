import os
from aalpy.base.SUL import CacheSUL
from rers_sul import RERSSUL

for file_name in os.listdir("model_checker_output"):
    # if file_name.replace(".out", "") in ["m158", "m159", "m164", "m172", "m181", "m183", "m54", "m95", "m167", "m173",
    #                                      "m182", "m189", "m190", "m196", "m199", "m22", "m27", "m41", "m135", "m76", "m132", "m49", "m131"]:
    #     continue
    # if file_name.replace(".out", "") in ["m54","m183","m196","m45"]:
    #     continue
    if file_name.replace(".out", "") not in ["m185"]:
        continue
    print(file_name)
    with open(f"model_checker_output/{file_name}") as f:
        all_data = f.read()
        for i in range(0, 100):
            word = []
            first = all_data.find(f"start looking for error {i}")
            second = all_data.find(f"done looking for error {i}")
            data = all_data[first:second]

            a = data.find("String[] inputs = {")
            l_str = data[a + len("String[] inputs = {"):data.find("}", a)]
            alphabet = l_str.replace('"', "").split(",")
            transitions_split = data.split("- transition #")
            for transitions_str in transitions_split[2:]:
                idx_str = transitions_str[transitions_str.find("cur=") + len("cur="):transitions_str.find("]")]
                word.append(alphabet[int(idx_str)])
            if "java.lang.AssertionError  at Errors.__VERIFIER_err" not in data:
                print("*", end="")
                # continue
            # if 'usr2_ai1_VoidReply' in word:
            #     continue
            if len(word) >= 15:
                print(i, len(word), len(set(word)), word, sep=";")
            # print(word, ",")

            # benchmark = file_name.replace(".out", "")
            #
            # sul = CacheSUL(RERSSUL(benchmark=benchmark, for_T=False, is_prefix_closed=False, is_suffix_closed=True))
            #
            # print(sul.query(tuple(word)))
