import pandas as pd
import numpy as np
import patsy
from sklearn.linear_model import LogisticRegression, LinearRegression

def ipw(df: pd.DataFrame, ps_formula: str, T: str, Y: str) -> float:
    """
    Calculate the Average Treatment Effect using Inverse Propensity Weighting
    
    Params:
    
        df : pd.DataFrame
            The dataset containing treatment, outcome, and covariates
        ps_formula : str
            Formula for propensity score model (e.g., "X1 + X2 + X3")
        T : str
            Name of the treatment column
        Y : str
            Name of the outcome column
    
    Returns:
    
        ate: float
            The estimated Average Treatment Effect (ATE)
    """
    # Convert formula to design matrix using patsy
    X = patsy.dmatrix(ps_formula, df, return_type='dataframe')
    
    # Fit propensity score model
    model = LogisticRegression(penalty=None, max_iter=1000)
    model.fit(X, df[T])
    
    # Get propensity scores (probability of treatment)
    ps = model.predict_proba(X)[:, 1]
    
    # Calculate ATE using the IPW formula
    # ATE = E[(T - e(X)) / (e(X) × (1 - e(X))) × Y]
    treatment = df[T].values
    outcome = df[Y].values
    
    # Calculate the IPW estimator
    weights = (treatment - ps) / (ps * (1 - ps))
    ate = (weights * outcome).mean()
    
    return ate

def doubly_robust(df: pd.DataFrame, formula: str, T: str, Y: str) -> float:
    """
    Calculate the Average Treatment Effect using Doubly Robust Estimation
    
    Params:
    
        df : pd.DataFrame
            The dataset containing treatment, outcome, and covariates
        formula : str
            Formula for both propensity score and outcome models (e.g., "X1 + X2 + X3")
        T : str
            Name of the treatment column
        Y : str
            Name of the outcome column
    
    Returns:
        ate: float
            The estimated Average Treatment Effect (ATE)
    """
    # Convert formula to design matrix using patsy
    X = patsy.dmatrix(formula, df, return_type='dataframe')
    
    # Fit propensity score model
    ps_model = LogisticRegression(penalty=None, max_iter=1000)
    ps_model.fit(X, df[T])
    
    # Get propensity scores (probability of treatment)
    e_x = ps_model.predict_proba(X)[:, 1]
    
    # Get treatment and outcome arrays
    treatment = df[T].values
    outcome = df[Y].values
    
    # Fit outcome model for control group (T=0)
    X_control = X[df[T] == 0]
    Y_control = df.loc[df[T] == 0, Y]
    mu_0_model = LinearRegression()
    mu_0_model.fit(X_control, Y_control)
    
    # Fit outcome model for treated group (T=1)
    X_treated = X[df[T] == 1]
    Y_treated = df.loc[df[T] == 1, Y]
    mu_1_model = LinearRegression()
    mu_1_model.fit(X_treated, Y_treated)
    
    # Get predictions for all observations from both outcome models
    mu_0 = mu_0_model.predict(X)
    mu_1 = mu_1_model.predict(X)
    
    # Calculate ATE using the Doubly Robust formula
    # ATE = E[T(Y - μ₁(X))/e(X) + μ₁(X)] - E[(1-T)(Y - μ₀(X))/(1-e(X)) + μ₀(X)]
    
    # Treated component
    treated_component = (treatment * (outcome - mu_1) / e_x) + mu_1
    
    # Control component
    control_component = ((1 - treatment) * (outcome - mu_0) / (1 - e_x)) + mu_0
    
    # ATE is the difference of expectations
    ate = treated_component.mean() - control_component.mean()
    
    return ate