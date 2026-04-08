import pandas as pd
import numpy as np

df = pd.read_csv("Loan_Data.csv")

df = df.sort_values('fico_score').reset_index(drop=True)
def log_likelihood(n, k):
    if k == 0 or k == n:
        return 0  # avoid log(0)
    
    p = k / n
    return k * np.log(p) + (n - k) * np.log(1 - p)
n = len(df)

cum_defaults = df['default'].cumsum()
def get_bucket_stats(start, end):
    n_i = end - start + 1
    k_i = cum_defaults[end] - (cum_defaults[start-1] if start > 0 else 0)
    return n_i, k_i
def optimal_buckets(num_buckets):
    dp = np.full((n, num_buckets+1), -np.inf)
    split = np.zeros((n, num_buckets+1), dtype=int)
    
    # Base case: 1 bucket
    for i in range(n):
        n_i, k_i = get_bucket_stats(0, i)
        dp[i][1] = log_likelihood(n_i, k_i)
    
    # Fill DP table
    for b in range(2, num_buckets+1):
        for i in range(n):
            for j in range(i):
                n_i, k_i = get_bucket_stats(j+1, i)
                score = dp[j][b-1] + log_likelihood(n_i, k_i)
                
                if score > dp[i][b]:
                    dp[i][b] = score
                    split[i][b] = j
    
    return dp, split
def get_boundaries(split, num_buckets):
    boundaries = []
    i = n - 1
    
    for b in range(num_buckets, 1, -1):
        j = split[i][b]
        boundaries.append(df['fico_score'][j])
        i = j
    
    return sorted(boundaries)
num_buckets = 5

dp, split = optimal_buckets(num_buckets)
boundaries = get_boundaries(split, num_buckets)

print("Optimal boundaries:", boundaries)
def assign_rating(fico_score, boundaries):
    for i, boundary in enumerate(boundaries):
        if fico_score <= boundary:
            return len(boundaries) - i + 1
    return 1