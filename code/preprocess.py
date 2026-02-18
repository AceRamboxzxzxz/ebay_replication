import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('input/PaidSearch.csv')

# Convert date to datetime (explicit format avoids warnings)
df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y')

# Create log revenue
df['log_revenue'] = np.log(df['revenue'])

# Step 2 — Separate treated and untreated units
treated = df[df['search_stays_on'] == 0].copy()
untreated = df[df['search_stays_on'] == 1].copy()

# For each group, create pivot table: dma index, treatment_period columns, mean(log_revenue) values
treated_pivot = treated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)
untreated_pivot = untreated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

# Rename columns
treated_pivot = treated_pivot.rename(columns={0: 'log_revenue_pre', 1: 'log_revenue_post'})
untreated_pivot = untreated_pivot.rename(columns={0: 'log_revenue_pre', 1: 'log_revenue_post'})

# Compute difference: post - pre
treated_pivot['log_revenue_diff'] = treated_pivot['log_revenue_post'] - treated_pivot['log_revenue_pre']
untreated_pivot['log_revenue_diff'] = untreated_pivot['log_revenue_post'] - untreated_pivot['log_revenue_pre']

# Save pivot tables
os.makedirs('temp', exist_ok=True)
treated_pivot.to_csv('temp/treated_pivot.csv')
untreated_pivot.to_csv('temp/untreated_pivot.csv')

# Step 3 — Print summary statistics
n_treated_dmas = treated['dma'].nunique()
n_untreated_dmas = untreated['dma'].nunique()
date_min = df['date'].min().date()
date_max = df['date'].max().date()

print(f"Treated DMAs: {n_treated_dmas}")
print(f"Untreated DMAs: {n_untreated_dmas}")
print(f"Date range: {date_min} to {date_max}")

# Step 4 — Reproduce Figure 5.2
# Group by date and search_stays_on, mean revenue
daily_rev = df.groupby(['date', 'search_stays_on'], as_index=False)['revenue'].mean()

control = daily_rev[daily_rev['search_stays_on'] == 1]
treat = daily_rev[daily_rev['search_stays_on'] == 0]

# Make sure output folder exists
os.makedirs('output/figures', exist_ok=True)

plt.figure()
plt.plot(control['date'], control['revenue'], label='Control (search stays on)')
plt.plot(treat['date'], treat['revenue'], label='Treatment (search goes off)')

# Vertical dashed line at treatment start date
plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')

plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title("Average revenue over time: treatment vs control")
plt.legend()
plt.tight_layout()
plt.savefig('output/figures/figure_5_2.png', dpi=200)
plt.close()

# Step 5 — Reproduce Figure 5.3
# Group by date and search_stays_on, mean log_revenue
daily_log = df.groupby(['date', 'search_stays_on'], as_index=False)['log_revenue'].mean()

# Pivot so each date has a column for each group (0=treat, 1=control)
daily_log_pivot = daily_log.pivot(index='date', columns='search_stays_on', values='log_revenue')

# Compute difference: log(avg control rev) - log(avg treatment rev)
daily_log_pivot['log_diff'] = daily_log_pivot[1] - daily_log_pivot[0]

plt.figure()
plt.plot(daily_log_pivot.index, daily_log_pivot['log_diff'])

# Vertical dashed line at treatment start date
plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')

plt.xlabel('Date')
plt.ylabel('log(rev_control) - log(rev_treat)')
plt.title('Log-scale revenue difference over time (control - treatment)')
plt.tight_layout()
plt.savefig('output/figures/figure_5_3.png', dpi=200)
plt.close()

