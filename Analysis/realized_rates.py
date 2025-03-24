import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, chi2_contingency

# Load the dataset
df = pd.read_csv(os.path.join("Data", "SFU_1324_Conversion_rate.csv"))

# Clean GPA column (remove missing values)
df = df[df["GPA"].notna()]

# Convert Funding column to binary (Yes = 1, No = 0)
df["Funding"] = df["Funding"].replace({
    "Yes": 1,
    "No": 0
})

df["Prior International Experience"] = df["Prior International Experience"].replace({
    "Yes": 1,
    "No": 0
})

df["Co-op Participation"] = df["Co-op Participation"].replace({
    "Yes": 1,
    "No": 0
})

# Define completion based on "Approved → Realized" conversion rate
df["Realization Status"] = np.where(df["Approved → Realized"].notna() & (df["Approved → Realized"] > 0), "Realized", "Not Realized")

### 1. Compare GPA of Realized vs. Not Realized Students
Realized = df[df["Realization Status"] == "Realized"]["GPA"]
not_Realized = df[df["Realization Status"] == "Not Realized"]["GPA"]

# T-test to check if GPA differences are statistically significant
t_stat, p_value = ttest_ind(Realized, not_Realized, nan_policy='omit')

plt.figure(figsize=(10, 5))
sns.set_style("whitegrid")  # Use a clean grid style
palette = sns.color_palette("coolwarm")  # More vibrant colors

sns.boxplot(x=df["Realization Status"], y=df["GPA"], palette=palette)
plt.title("GPA Distribution: Realized vs. Not Realized", fontsize=14, fontweight="bold")
plt.ylabel("GPA", fontsize=12)
plt.xlabel("Realization Status", fontsize=12)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.savefig(os.path.join("Plots", "gpa_distr.png"), dpi=300)

print(f"T-test for GPA Difference: t-statistic={t_stat:.2f}, p-value={p_value:.4f}")

### 2. Funding vs. Realized Rate
funding_table = pd.crosstab(df["Funding"], df["Realization Status"])
chi2, p_funding, _, _ = chi2_contingency(funding_table)

funding_rates = df.groupby("Funding")["Approved → Realized"].mean()
funding_rates.to_csv(os.path.join("Data", "Funding_Conv_Rates.csv"))

print("\nFunding Impact on Realized Rates:")
print(funding_rates)
print(f"Chi-square test for Funding vs Realized: p-value={p_funding:.4f}")

# Funding Visualization
plt.figure(figsize=(8, 5))
sns.barplot(x=funding_rates.index, y=funding_rates.values, palette="viridis", edgecolor="black")
plt.title("Realization Rates by Funding", fontsize=14, fontweight="bold")
plt.ylabel("Realization Rate (%)", fontsize=12)
plt.xlabel("Funding", fontsize=12)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig(os.path.join("Plots", "funding_rate.png"), dpi=300)

### 3. Motivation vs. Realized Rate
motivation_rates = df.groupby("Motivation")["Approved → Realized"].mean()
motivation_rates.to_csv(os.path.join("Data", "Motivation_Conv_Rates.csv"))

print("\nRealization Rates by Motivation:")
print(motivation_rates)

# Motivation Visualization
plt.figure(figsize=(8, 5))
sns.barplot(x=motivation_rates.index, y=motivation_rates.values, palette="magma", edgecolor="black", alpha=0.85)
plt.title("Realization Rates by Motivation", fontsize=14, fontweight="bold")
plt.ylabel("Realization Rate (%)", fontsize=12)
plt.xlabel("Motivation", fontsize=12)
plt.xticks(rotation=30, ha="right", fontsize=11)
plt.yticks(fontsize=11)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig(os.path.join("Plots", "motivation_rate.png"), dpi=300)

### 4. Prior International Experience vs. Realized Rate
intlexp_table = pd.crosstab(df["Prior International Experience"], df["Realization Status"])
chi2, p_intlexp, _, _ = chi2_contingency(intlexp_table)

intlexp_rates = df.groupby("Prior International Experience")["Approved → Realized"].mean()
intlexp_rates.to_csv(os.path.join("Data", "IntlExp_Conv_Rates.csv"))

print("\nPrior International Experience on Realized Rates:")
print(intlexp_rates)
print(f"Chi-square test for Prior International Experience vs Realized: p-value={p_intlexp:.4f}")

# International Experience Visualization
plt.figure(figsize=(10, 5))
sns.barplot(x=intlexp_rates.index, y=intlexp_rates.values, palette="cividis", edgecolor="black", alpha=0.85)
plt.title("Realization Rates by Prior International Experience", fontsize=14, fontweight="bold")
plt.ylabel("Realization Rate (%)", fontsize=12)
plt.xlabel("Prior International Experience", fontsize=12)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig(os.path.join("Plots", "international_expr_rate.png"), dpi=300)

### 5. Co-op Participation vs. Realized Rate
coop_table = pd.crosstab(df["Co-op Participation"], df["Realization Status"])
chi2, p_coop, _, _ = chi2_contingency(coop_table)

coop_rates = df.groupby("Co-op Participation")["Approved → Realized"].mean()
coop_rates.to_csv(os.path.join("Data", "Coop_Conv_Rates.csv"))

print("\nCo-op Participation on Realized Rates:")
print(coop_rates)
print(f"Chi-square test for Co-op Participation vs Realized: p-value={p_coop:.4f}")

# Co-op Visualization
plt.figure(figsize=(10, 5))
sns.barplot(x=coop_rates.index, y=coop_rates.values, palette="coolwarm", edgecolor="black", alpha=0.85)
plt.title("Realization Rates by Co-op Participation", fontsize=14, fontweight="bold")
plt.ylabel("Realization Rate (%)", fontsize=12)
plt.xlabel("Co-op Participation", fontsize=12)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig(os.path.join("Plots", "coop_rate.png"), dpi=300)


