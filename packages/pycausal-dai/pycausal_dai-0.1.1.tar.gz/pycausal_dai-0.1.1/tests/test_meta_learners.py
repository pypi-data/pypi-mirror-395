import pandas as pd
import numpy as np
from pycausal_dai.meta_learners import s_learner_discrete, t_learner_discrete, x_learner_discrete, double_ml_cate


def simple_data():
    """Generate simple data with known treatment effect"""
    np.random.seed(42)
    n = 1000
    
    # Covariates
    x1 = np.random.normal(0, 1, n)
    x2 = np.random.normal(0, 1, n)
    
    # Treatment assignment (confounded)
    prob_t = 1 / (1 + np.exp(-(0.5 * x1 + 0.3 * x2)))
    t = np.random.binomial(1, prob_t, n)
    
    # Outcome with constant treatment effect = 2.0
    y = 2.0 * t + x1 + 0.5 * x2 + np.random.normal(0, 0.5, n)
    
    df = pd.DataFrame({'x1': x1, 'x2': x2, 't': t, 'y': y})
    
    # Split into train/test
    train = df.iloc[:800].copy()
    test = df.iloc[800:].copy()
    
    return train, test


def continuous_treatment_data():
    """Generate data with continuous treatment"""
    np.random.seed(789)
    n = 1000
    
    # Covariates
    x1 = np.random.normal(0, 1, n)
    x2 = np.random.normal(0, 1, n)
    
    # Continuous treatment
    t = 10 + x1 + 2*x2 + np.random.normal(0, 1, n)
    
    # Outcome: linear effect of treatment
    y = t + x1 + 0.5*x2 + np.random.normal(0, 0.5, n)
    
    df = pd.DataFrame({'x1': x1, 'x2': x2, 't': t, 'y': y})
    
    train = df.iloc[:800].copy()
    test = df.iloc[800:].copy()
    
    return train, test


def test_s_learner_returns_dataframe():
    """Test that s_learner_discrete returns a DataFrame"""
    # Generate test data
    train, test = simple_data()
    
    # Call function under test
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    # Assert expected behavior
    assert isinstance(result, pd.DataFrame)


def test_s_learner_has_cate_column():
    """Test that s_learner_discrete result has 'cate' column"""
    # Generate test data
    train, test = simple_data()
    
    # Call function under test
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    # Assert 'cate' column exists
    assert 'cate' in result.columns


def test_s_learner_constant_effect():
    """Test that s_learner_discrete recovers the true constant treatment effect"""
    # Generate test data with known constant effect = 2.0
    train, test = simple_data()
    
    # Call function under test
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    # Estimate average treatment effect
    estimated_ate = result['cate'].mean()
    true_effect = 2.0
    
    # Assert the estimated effect is close to true effect (with tolerance)
    assert abs(estimated_ate - true_effect) < 0.5


def test_s_learner_return_numeric_cate():
    """Test that s_learner_discrete returns numeric CATE values"""
    # Generate test data
    train, test = simple_data()
    
    # Call function under test
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    # Assert CATE column is numeric
    assert pd.api.types.is_numeric_dtype(result['cate'])


def test_s_learner_no_nan_values():
    """Test that s_learner_discrete produces no NaN values in CATE"""
    # Generate test data
    train, test = simple_data()
    
    # Call function under test
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    # Assert no NaN values in CATE
    assert not result['cate'].isna().any()


def test_t_learner_returns_dataframe():
    """Test that t_learner_discrete returns a DataFrame"""
    # Generate test data
    train, test = simple_data()
    
    # Call function under test
    result = t_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    # Assert expected behavior
    assert isinstance(result, pd.DataFrame)


def test_x_learner_returns_dataframe():
    """Test that x_learner_discrete returns a DataFrame"""
    # Generate test data
    train, test = simple_data()
    
    # Call function under test
    result = x_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    # Assert expected behavior
    assert isinstance(result, pd.DataFrame)


def test_double_ml_returns_dataframe():
    """Test that double_ml_cate returns a DataFrame"""
    # Generate test data
    train, test = simple_data()
    
    # Call function under test
    result = double_ml_cate(train, test, ['x1', 'x2'], 't', 'y')
    
    # Assert expected behavior
    assert isinstance(result, pd.DataFrame)


def test_double_ml_continuous_treatment():
    """Test that double_ml_cate works with continuous treatment"""
    # Generate test data with continuous treatment
    train, test = continuous_treatment_data()
    
    # Call function under test
    result = double_ml_cate(train, test, ['x1', 'x2'], 't', 'y')
    
    # Assert it returns a DataFrame with CATE column
    assert isinstance(result, pd.DataFrame)
    assert 'cate' in result.columns
    
    # Assert CATE is numeric and has no NaN values
    assert pd.api.types.is_numeric_dtype(result['cate'])
    assert not result['cate'].isna().any()
    
    # For continuous treatment where y = t + x1 + 0.5*x2 + noise,
    # the treatment effect should be approximately 1.0
    estimated_ate = result['cate'].mean()
    true_effect = 1.0
    assert abs(estimated_ate - true_effect) < 0.5