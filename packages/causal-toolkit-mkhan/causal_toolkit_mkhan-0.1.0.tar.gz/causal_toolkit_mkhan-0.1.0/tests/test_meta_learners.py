# Pytest tests for meta-learner functions

import numpy as np
import pandas as pd
from causal_toolkit_mkhan.meta_learners import s_learner_discrete, t_learner_discrete, x_learner_discrete, double_ml_cate


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


# ========================================
# S-Learner Tests (5 tests)
# ========================================

def test_s_learner_returns_dataframe():
    """Test that s_learner_discrete returns a DataFrame"""
    # 1. Generate test data
    train, test = simple_data()
    
    # 2. Call function under test
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    # 3. Assert expected behavior
    assert isinstance(result, pd.DataFrame)


def test_s_learner_has_cate_column():
    """Test that s_learner_discrete result has 'cate' column"""
    train, test = simple_data()
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    assert 'cate' in result.columns


def test_s_learner_constant_effect():
    """Test that s_learner_discrete recovers the true constant effect"""
    train, test = simple_data()
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    # True effect is 2.0
    estimated_ate = result['cate'].mean()
    true_effect = 2.0
    tolerance = 0.5  # Use reasonable tolerance for statistical estimation
    
    assert abs(estimated_ate - true_effect) < tolerance


def test_s_learner_return_numeric_cate():
    """Test that s_learner_discrete returns numeric CATE values"""
    train, test = simple_data()
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    assert pd.api.types.is_numeric_dtype(result['cate'])


def test_s_learner_no_nan_values():
    """Test that s_learner_discrete has no NaN values in CATE"""
    train, test = simple_data()
    result = s_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    assert not result['cate'].isna().any()


# ========================================
# T-Learner Tests (1 test)
# ========================================

def test_t_learner_returns_dataframe():
    """Test that t_learner_discrete returns a DataFrame"""
    train, test = simple_data()
    result = t_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    assert isinstance(result, pd.DataFrame)


# ========================================
# X-Learner Tests (1 test)
# ========================================

def test_x_learner_returns_dataframe():
    """Test that x_learner_discrete returns a DataFrame"""
    train, test = simple_data()
    result = x_learner_discrete(train, test, ['x1', 'x2'], 't', 'y')
    
    assert isinstance(result, pd.DataFrame)


# ========================================
# Double ML Tests (2 tests)
# ========================================

def test_double_ml_returns_dataframe():
    """Test that double_ml_cate returns a DataFrame"""
    train, test = simple_data()
    result = double_ml_cate(train, test, ['x1', 'x2'], 't', 'y')
    
    assert isinstance(result, pd.DataFrame)


def test_double_ml_continuous_treatment():
    """Test that double_ml_cate works with continuous treatment"""
    train, test = continuous_treatment_data()
    result = double_ml_cate(train, test, ['x1', 'x2'], 't', 'y')
    
    # Should return DataFrame with cate column
    assert isinstance(result, pd.DataFrame)
    assert 'cate' in result.columns
    assert pd.api.types.is_numeric_dtype(result['cate'])
    assert not result['cate'].isna().any()

