import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold


def s_learner_discrete(train, test, X, T, y) -> pd.DataFrame:
    """
    S-Learner: Single model approach for CATE estimation.
    Fits one model using both covariates and treatment, then compares predictions.
    """
    # Fit single model on all data with treatment as a feature
    model = LGBMRegressor()
    model.fit(train[X + [T]], train[y])
    
    # Create copies of test data with treatment set to 0 and 1
    test_t0 = test[X].copy()
    test_t0[T] = 0
    
    test_t1 = test[X].copy()
    test_t1[T] = 1
    
    # Predict under both treatment conditions
    pred_t0 = model.predict(test_t0[X + [T]])
    pred_t1 = model.predict(test_t1[X + [T]])
    
    # CATE is the difference
    result = test.copy()
    result['cate'] = pred_t1 - pred_t0
    
    return result


def t_learner_discrete(train, test, X, T, y) -> pd.DataFrame:
    """
    T-Learner: Two separate models for treated and control groups.
    """
    # Split training data by treatment
    train_control = train[train[T] == 0]
    train_treated = train[train[T] == 1]
    
    # Fit separate models for control and treated groups
    model_0 = LGBMRegressor()
    model_0.fit(train_control[X], train_control[y])
    
    model_1 = LGBMRegressor()
    model_1.fit(train_treated[X], train_treated[y])
    
    # Predict on test set with both models
    pred_0 = model_0.predict(test[X])
    pred_1 = model_1.predict(test[X])
    
    # CATE is the difference
    result = test.copy()
    result['cate'] = pred_1 - pred_0
    
    return result


def x_learner_discrete(train, test, X, T, y) -> pd.DataFrame:
    """
    X-Learner: Advanced meta-learner using propensity scores for weighting.
    """
    # Stage 1: Fit outcome models like T-Learner
    train_control = train[train[T] == 0]
    train_treated = train[train[T] == 1]
    
    model_0 = LGBMRegressor()
    model_0.fit(train_control[X], train_control[y])
    
    model_1 = LGBMRegressor()
    model_1.fit(train_treated[X], train_treated[y])
    
    # Stage 2: Compute pseudo-treatment effects
    # For control units: τ̂₀(xᵢ) = μ₁(xᵢ) - yᵢ
    tau_0 = model_1.predict(train_control[X]) - train_control[y].values
    
    # For treated units: τ̂₁(xᵢ) = yᵢ - μ₀(xᵢ)
    tau_1 = train_treated[y].values - model_0.predict(train_treated[X])
    
    # Fit models for τ₀(x) and τ₁(x)
    tau_model_0 = LGBMRegressor()
    tau_model_0.fit(train_control[X], tau_0)
    
    tau_model_1 = LGBMRegressor()
    tau_model_1.fit(train_treated[X], tau_1)
    
    # Estimate propensity scores
    propensity_model = LogisticRegression(penalty=None)
    propensity_model.fit(train[X], train[T])
    e_x = propensity_model.predict_proba(test[X])[:, 1]
    
    # Predict τ₀ and τ₁ on test set
    tau_0_pred = tau_model_0.predict(test[X])
    tau_1_pred = tau_model_1.predict(test[X])
    
    # Final estimate: CATE(x) = e(x)·τ₀(x) + (1-e(x))·τ₁(x)
    result = test.copy()
    result['cate'] = e_x * tau_0_pred + (1 - e_x) * tau_1_pred
    
    return result


def double_ml_cate(train, test, X, T, y) -> pd.DataFrame:
    """
    Double Machine Learning for CATE estimation with continuous treatment.
    Uses cross-fitting to partial out confounders from both treatment and outcome.
    """
    n_folds = 5
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    
    # Initialize residuals
    T_res_train = np.zeros(len(train))
    Y_res_train = np.zeros(len(train))
    
    # Cross-fitting: partial out X from T and Y
    for train_idx, val_idx in kf.split(train):
        # Split data
        train_fold = train.iloc[train_idx]
        val_fold = train.iloc[val_idx]
        
        # Model for T ~ X
        model_T = LGBMRegressor()
        model_T.fit(train_fold[X], train_fold[T])
        T_pred = model_T.predict(val_fold[X])
        T_res_train[val_idx] = val_fold[T].values - T_pred
        
        # Model for Y ~ X
        model_Y = LGBMRegressor()
        model_Y.fit(train_fold[X], train_fold[y])
        Y_pred = model_Y.predict(val_fold[X])
        Y_res_train[val_idx] = val_fold[y].values - Y_pred
    
    # Create transformed outcome and weights
    # Avoid division by zero or very small numbers
    T_res_train_safe = np.where(np.abs(T_res_train) < 1e-10, 1e-10, T_res_train)
    Y_star = Y_res_train / T_res_train_safe
    weights = T_res_train ** 2
    
    # Fit CATE model
    cate_model = LGBMRegressor()
    cate_model.fit(train[X], Y_star, sample_weight=weights)
    
    # Predict CATE on test set
    result = test.copy()
    result['cate'] = cate_model.predict(test[X])
    
    return result