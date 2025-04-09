import scipy.stats as stats
import pandas as pd

# Cleaned and usable subset of the data
data = {
    "System": [
        "m24", "m45", "m54", "m76", "m95", "m135", "m158", "m159", "m172", "m181", "m183", "m201",
        "m22", "m27", "m41", "m106", "m132", "m173", "m182", "m189", "m199"
    ],
    "cex_len": [10, 5, 5, 8, 5, 13, 5, 6, 10, 6, 5, 7, 9, 9, 5, 11, 5, 6, 6, 7, 7],
    "Sigma_size": [22, 12, 10, 17, 15, 23, 17, 22, 19, 20, 12, 19, 23, 25, 22, 24, 20, 21, 14, 21, 20],
    "T_size": [512, 32, 16, 256, 32, 1024, 32, 64, 64, 64, 32, 64, 512, 64, 32, 1024, 32, 64, 32, 128, 128],
    "DFA_size": [21, 9, 134, 268, 39, 31, 33, 48, 20, 20, 60, 25, 56, 43, 39, 13, 14, 32, 12, 17, 139],
    "Time_sec": [142, 100, 6094, 886, 92, 221, 51, 111, 108, 10016, 602, 280, 390, 106, 377, 283, 19405, 1015, 1184, 83, 199],
    "FE": [4, 4, 7, 3, 3, 4, 6, 8, 4, 3, 25, 4, 4, 6, 9, 3, 3, 3, 4, 3, 4],
    "EDFE": [4, 3, 7, 3, 3, 4, 4, 4, 4, 3, 8, 4, 6, 6, 5, 3, 4, 3, 3, 3, 4],
    "B": [12, 7, 20, 10, 7, 15, 7, 8, 12, 8, 9, 9, 11, 11, 11, 13, 8, 8, 9, 9, 10],
}

df = pd.DataFrame(data)

# Mann-Whitney U tests
mw_FE_B = stats.mannwhitneyu(df["FE"], df["B"], alternative="less")
mw_EDFE_B = stats.mannwhitneyu(df["EDFE"], df["B"], alternative="less")
mw_FE_EDFE = stats.mannwhitneyu(df["FE"], df["EDFE"], alternative="two-sided")

# Spearman correlations
correlations = {
    "B vs cex_len": stats.spearmanr(df["B"], df["cex_len"]),
    "B vs Sigma": stats.spearmanr(df["B"], df["Sigma_size"]),
    "B vs DFA": stats.spearmanr(df["B"], df["DFA_size"]),
    "B vs T": stats.spearmanr(df["B"], df["T_size"]),
    "FE vs DFA": stats.spearmanr(df["FE"], df["DFA_size"]),
    "EDFE vs DFA": stats.spearmanr(df["EDFE"], df["DFA_size"]),
    "FE vs EDFE": stats.spearmanr(df["FE"], df["EDFE"]),
    "Time vs DFA": stats.spearmanr(df["Time_sec"], df["DFA_size"]),
}

# Summarize results
results = {
    "Mann-Whitney FE < B p-value": mw_FE_B.pvalue,
    "Mann-Whitney EDFE < B p-value": mw_EDFE_B.pvalue,
    "Mann-Whitney FE ≠ EDFE p-value": mw_FE_EDFE.pvalue,
}

# Add correlation results
for label, (rho, pval) in correlations.items():
    results[f"Spearman {label} rho"] = rho
    results[f"Spearman {label} p-value"] = pval


print(results)