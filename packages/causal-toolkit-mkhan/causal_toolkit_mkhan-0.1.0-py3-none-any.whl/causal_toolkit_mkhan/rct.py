from typing import Tuple
import numpy as np
import pandas as pd
from scipy import stats


def _split_groups(data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Return Y arrays for T=1 and T=0"""
    y1 = data.loc[data["T"] == 1, "Y"].to_numpy(dtype=float)
    y0 = data.loc[data["T"] == 0, "Y"].to_numpy(dtype=float)
    return y1, y0


def _se_diff_means(y1: np.ndarray, y0: np.ndarray) -> float:
    """SE(ȳ1 − ȳ0) with Welch form"""
    s1, s0 = y1.var(ddof=1), y0.var(ddof=1)
    n1, n0 = y1.size, y0.size
    return float(np.sqrt(s1 / n1 + s0 / n0))


def calculate_ate_ci(data: pd.DataFrame, alpha: float = 0.05) -> Tuple[float, float, float]:
    """Return (ATE, CI_low, CI_high) with z-based CI"""
    y1, y0 = _split_groups(data)
    ate = float(y1.mean() - y0.mean())
    se = _se_diff_means(y1, y0)
    z = stats.norm.ppf(1 - alpha / 2.0)
    return ate, ate - z * se, ate + z * se


def calculate_ate_pvalue(data: pd.DataFrame) -> Tuple[float, float, float]:
    """Return (ATE, t_stat, two_sided_p)."""
    y1, y0 = _split_groups(data)
    ate = float(y1.mean() - y0.mean())
    se = _se_diff_means(y1, y0)
    t = ate / se
    p = 2.0 * (1.0 - stats.norm.cdf(abs(t)))
    return ate, float(t), float(p)

