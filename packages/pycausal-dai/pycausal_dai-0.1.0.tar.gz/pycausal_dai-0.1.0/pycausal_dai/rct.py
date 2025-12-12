import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple

def calculate_ate_ci(data: pd.DataFrame, alpha: float = 0.05) -> Tuple[float, float, float]:

    # ATE_estimate: The estimated average treatment effect
    # CI_lower: Lower bound of the confidence interval
    # CI_upper: Upper bound of the confidence interval

    # ATE = E[Y|T=1] - E[Y|T=0]
    # Standard Error: SE(ATE) = sqrt(Var(Y|T=1)/n₁ + Var(Y|T=0)/n₀)
    # Confidence Interval: ATE ± z_(α/2) × SE(ATE)
    
    t1 = data[data['T'] == 1]
    t0 = data[data['T'] == 0]
    eyt1 = np.mean(t1['Y'])
    eyt0 = np.mean(t0['Y'])
    ATE = eyt1 - eyt0
    se = np.sqrt(np.var(t1['Y'])/len(t1) + np.var(t0['Y'])/len(t0))

    z_crit = stats.norm.ppf(1-alpha/2)
    left = ATE - z_crit * se
    right = ATE + z_crit * se
    return (float(ATE), float(left), float(right))
    
def calculate_ate_pvalue(data: pd.DataFrame) -> Tuple[float, float, float]:
    
    # ATE_estimate: The estimated average treatment effect
    # t_statistic: The test statistic
    # p_value: The two-sided p-value

    # Null Hypothesis: H₀: ATE = 0
    # Alternative Hypothesis: H₁: ATE ≠ 0
    # Test Statistic: t = (ATE_estimate - 0) / SE(ATE)
    # P-value: 2 × (1 - Φ(|t|)) where Φ is the standard normal CDF

    t1 = data[data['T'] == 1]
    t0 = data[data['T'] == 0]
    eyt1 = np.mean(t1['Y'])
    eyt0 = np.mean(t0['Y'])
    ATE = eyt1 - eyt0
    se = np.sqrt(np.var(t1['Y'])/len(t1) + np.var(t0['Y'])/len(t0))

    t = ATE/se
    p = 2 * (1-stats.norm().cdf(np.abs(t)))
    return (float(ATE), float(t), float(p))