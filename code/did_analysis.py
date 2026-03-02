

# DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex



# did_analysis.py — DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Method: Compare pre-post log revenue changes between treatment and control DMAs.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex
# Reference: Blake et al. (2014), Taddy Ch. 5

import pandas as pd
import numpy as np
import os

# Load pivot tables
treated = pd.read_csv("temp/treated_pivot.csv", index_col=0)
untreated = pd.read_csv("temp/untreated_pivot.csv", index_col=0)

# Compute log revenue
treated_log = np.log(treated)
untreated_log = np.log(untreated)

# Compute pre-post change for each DMA
treated_diff = treated_log.iloc[-1] - treated_log.iloc[0]
untreated_diff = untreated_log.iloc[-1] - untreated_log.iloc[0]

# Means
r1 = treated_diff.mean()
r0 = untreated_diff.mean()

# DID estimate
gamma_hat = r1 - r0

# Standard error
se = np.sqrt(treated_diff.var(ddof=1)/len(treated_diff) +
             untreated_diff.var(ddof=1)/len(untreated_diff))

# 95% confidence interval
ci_low = gamma_hat - 1.96*se
ci_high = gamma_hat + 1.96*se

print("Gamma hat:", round(gamma_hat, 4))
print("Std Error:", round(se, 4))
print("95% CI:", [round(ci_low,4), round(ci_high,4)])

# Save LaTeX table
os.makedirs("output/tables", exist_ok=True)

with open("output/tables/did_table.tex", "w") as f:
    f.write("\\begin{tabular}{lccc}\n")
    f.write("\\hline\n")
    f.write("Estimate & Std. Error & CI Low & CI High \\\\\n")
    f.write("\\hline\n")
    f.write(f"{gamma_hat:.4f} & {se:.4f} & {ci_low:.4f} & {ci_high:.4f} \\\\\n")
    f.write("\\hline\n")
    f.write("\\end{tabular}\n")
=======
# DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex

import os
import pandas as pd
import numpy as np

# Step 1 — Load the preprocessed data
# Load pivot tables saved by preprocess.py
treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')

# Step 2 — Compute the DID estimate
# Means of log_revenue_diff
r1_bar = treated_pivot['log_revenue_diff'].mean()
r0_bar = untreated_pivot['log_revenue_diff'].mean()

# DID estimate
gamma_hat = r1_bar - r0_bar

# Sample variances (pandas .var() uses ddof=1 by default)
var1 = treated_pivot['log_revenue_diff'].var()
var0 = untreated_pivot['log_revenue_diff'].var()

# Sample sizes
n1 = treated_pivot['log_revenue_diff'].count()
n0 = untreated_pivot['log_revenue_diff'].count()

# Standard error
se = np.sqrt(var1 / n1 + var0 / n0)

# 95% confidence interval
ci_lower = gamma_hat - 1.96 * se
ci_upper = gamma_hat + 1.96 * se

# Step 3 — Print results to the console
print("DID Results (Log Scale)")
print("=======================")
print(f"Gamma hat: {gamma_hat:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

# Step 4 — Output a LaTeX table fragment
os.makedirs('output/tables', exist_ok=True)

latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lc}
\hline
& Log Scale \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ \\
Standard Error & $%.4f$ \\
95\%% CI & $[%.4f, \; %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}""" % (gamma_hat, se, ci_lower, ci_upper)

with open('output/tables/did_table.tex', 'w') as f:
    f.write(latex)
>>>>>>> 5b74e3a7bc733e4bc0a240cea866efaf20c75429
