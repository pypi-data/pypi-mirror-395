# Causal Toolkit

[![Tests](https://github.com/mokhan95/causal-toolkit-mkhan/workflows/Tests/badge.svg)](https://github.com/mokhan95/causal-toolkit-mkhan/actions)
[![PyPI version](https://badge.fury.io/py/causal-toolkit-mkhan.svg)](https://pypi.org/project/causal-toolkit-mkhan/)

A Python package for causal inference methods including RCT analysis, propensity score methods, and meta-learners.

## Installation

```bash
pip install causal-toolkit-mkhan
```

### Development Installation

```bash
git clone https://github.com/mokhan95/causal-toolkit-mkhan.git
cd causal-toolkit-mkhan
pip install -e .
```

## Usage

### RCT Analysis

```python
from causal_toolkit_mkhan import calculate_ate_ci, calculate_ate_pvalue

ate, ci_lower, ci_upper = calculate_ate_ci(data)
ate, t_stat, p_value = calculate_ate_pvalue(data)
```

### Propensity Score Methods

```python
from causal_toolkit_mkhan import ipw, doubly_robust

ate_ipw = ipw(df, ps_formula="X1 + X2", T="treatment", Y="outcome")
ate_dr = doubly_robust(df, formula="X1 + X2", T="treatment", Y="outcome")
```

### Meta-Learners

```python
from causal_toolkit_mkhan import s_learner_discrete, t_learner_discrete, x_learner_discrete

result = s_learner_discrete(train, test, X=['x1', 'x2'], T='treatment', y='outcome')
result = t_learner_discrete(train, test, X=['x1', 'x2'], T='treatment', y='outcome')
result = x_learner_discrete(train, test, X=['x1', 'x2'], T='treatment', y='outcome')
```

### Double ML

```python
from causal_toolkit_mkhan import double_ml_cate

result = double_ml_cate(train, test, X=['x1', 'x2'], T='treatment', y='outcome')
```

## API Reference

### `calculate_ate_ci(data, alpha=0.05)`
Returns `(ate, ci_lower, ci_upper)` using z-test.

### `calculate_ate_pvalue(data)`
Returns `(ate, t_statistic, p_value)`.

### `ipw(df, ps_formula, T, Y)`
Inverse Propensity Weighting estimation.

### `doubly_robust(df, formula, T, Y)`
Doubly Robust estimation.

### `s_learner_discrete(train, test, X, T, y)`
S-learner for discrete treatment CATE estimation.

### `t_learner_discrete(train, test, X, T, y)`
T-learner for discrete treatment CATE estimation.

### `x_learner_discrete(train, test, X, T, y)`
X-learner for discrete treatment CATE estimation.

### `double_ml_cate(train, test, X, T, y)`
Double ML for continuous treatment CATE estimation.

## Testing

```bash
uv run pytest tests/ -v
```

## Dependencies

- pandas >= 1.3.0
- numpy >= 1.21.0
- scipy >= 1.7.0
- scikit-learn >= 1.0.0
- lightgbm >= 3.3.0
- patsy >= 0.5.0

## License

MIT License

## Author

mkhan (mohammadokhan95@gmail.com)
