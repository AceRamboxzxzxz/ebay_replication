# did_analysis.py — DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Method: Compare pre-post log revenue changes between treatment and control DMAs.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex
# Reference: Blake et al. (2014), Taddy Ch. 5

import os
import numpy as np
import pandas as pd


def main() -> None:
    # Load pivot tables saved by preprocess.py
    # These are expected to contain a column named 'log_revenue_diff'
    treated_pivot = pd.read_csv("temp/treated_pivot.csv", index_col=0)
    untreated_pivot = pd.read_csv("temp/untreated_pivot.csv", index_col=0)

    if "log_revenue_diff" not in treated_pivot.columns or "log_revenue_diff" not in untreated_pivot.columns:
        raise ValueError(
            "Expected 'log_revenue_diff' column in temp/treated_pivot.csv and temp/untreated_pivot.csv. "
            "Re-run preprocess.py or check the output format."
        )

    # DID estimate on log scale
    r1_bar = treated_pivot["log_revenue_diff"].mean()
    r0_bar = untreated_pivot["log_revenue_diff"].mean()
    gamma_hat = r1_bar - r0_bar

    # Standard error (independent samples)
    var1 = treated_pivot["log_revenue_diff"].var(ddof=1)
    var0 = untreated_pivot["log_revenue_diff"].var(ddof=1)
    n1 = treated_pivot["log_revenue_diff"].count()
    n0 = untreated_pivot["log_revenue_diff"].count()
    se = np.sqrt(var1 / n1 + var0 / n0)

    # 95% confidence interval (log scale)
    ci_lower = gamma_hat - 1.96 * se
    ci_upper = gamma_hat + 1.96 * se

    # Exponentiated (levels) results
    gamma_hat_exp = np.exp(gamma_hat)
    ci_lower_exp = np.exp(ci_lower)
    ci_upper_exp = np.exp(ci_upper)

    # Print results
    print("DID Results (Log Scale)")
    print("=======================")
    print(f"Gamma hat: {gamma_hat:.4f}")
    print(f"Std Error: {se:.4f}")
    print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

    # Write LaTeX table (two columns)
    os.makedirs("output/tables", exist_ok=True)

    latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lcc}
\hline
& Log Scale & Levels (exp) \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ & $%.4f$ \\
Standard Error & $%.4f$ & --- \\
95\%% CI & $[%.4f, \; %.4f]$ & $[%.4f, \; %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}""" % (
        gamma_hat,
        gamma_hat_exp,
        se,
        ci_lower,
        ci_upper,
        ci_lower_exp,
        ci_upper_exp,
    )

    with open("output/tables/did_table.tex", "w") as f:
        f.write(latex)


if __name__ == "__main__":
    main()




















