# Meta-learner implementations for causal inference
# - S-Learner (discrete T)
# - T-Learner (discrete T)
# - X-Learner (discrete T)
# - Double ML (continuous T)

from __future__ import annotations
from typing import List
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from lightgbm import LGBMRegressor


def _gbdt():
    """LightGBM regressor with quiet logs and stable defaults."""
    return LGBMRegressor(
        n_estimators=500,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=123,
        verbosity=-1,
    )


# -------------------------------
# 1) S-Learner (discrete T)
# -------------------------------
def s_learner_discrete(
    train: pd.DataFrame, test: pd.DataFrame, X: List[str], T: str, y: str
) -> pd.DataFrame:
    """
    Fit one model mu(X, T) -> Y, then CATE(x) = mu(x,1) - mu(x,0)
    """
    features = X + [T]
    mu = _gbdt()
    mu.fit(train[features], train[y])

    out = test.copy()
    x1 = out[X].copy(); x1[T] = 1
    x0 = out[X].copy(); x0[T] = 0
    out["cate"] = mu.predict(x1) - mu.predict(x0)
    return out


# -------------------------------
# 2) T-Learner (discrete T)
# -------------------------------
def t_learner_discrete(
    train: pd.DataFrame, test: pd.DataFrame, X: List[str], T: str, y: str
) -> pd.DataFrame:
    """
    Fit mu1 on T=1, mu0 on T=0, then CATE(x) = mu1(x) - mu0(x)
    """
    m0 = _gbdt()
    m1 = _gbdt()

    m0.fit(train.query(f"{T}==0")[X], train.query(f"{T}==0")[y])
    m1.fit(train.query(f"{T}==1")[X], train.query(f"{T}==1")[y])

    out = test.copy()
    out["cate"] = m1.predict(out[X]) - m0.predict(out[X])
    return out


# -------------------------------
# 3) X-Learner (discrete T)
# -------------------------------
def x_learner_discrete(
    train: pd.DataFrame, test: pd.DataFrame, X: List[str], T: str, y: str
) -> pd.DataFrame:
    """
    Stage 1: fit outcome models mu0, mu1 (as in T-learner)
    Stage 2: pseudo-effects:
        controls (T=0): tau0 = mu1(x) - y
        treated  (T=1): tau1 = y - mu0(x)
      Fit g0 on controls, g1 on treated.
    Blend with propensity e(x): CATE(x) = e(x)*g0(x) + (1-e(x))*g1(x)
    """
    mu0 = _gbdt()
    mu1 = _gbdt()
    mu0.fit(train.query(f"{T}==0")[X], train.query(f"{T}==0")[y])
    mu1.fit(train.query(f"{T}==1")[X], train.query(f"{T}==1")[y])

    idx0 = train[T] == 0
    idx1 = ~idx0

    tau0 = mu1.predict(train.loc[idx0, X]) - train.loc[idx0, y].to_numpy()
    tau1 = train.loc[idx1, y].to_numpy() - mu0.predict(train.loc[idx1, X])

    g0 = _gbdt()
    g1 = _gbdt()
    if idx0.sum() > 0:
        g0.fit(train.loc[idx0, X], tau0)
    if idx1.sum() > 0:
        g1.fit(train.loc[idx1, X], tau1)

    ps = LogisticRegression(penalty=None, solver="lbfgs", max_iter=2000)
    ps.fit(train[X], train[T])
    e_test = ps.predict_proba(test[X])[:, 1]

    out = test.copy()
    g0_pred = g0.predict(out[X]) if idx0.sum() > 0 else np.zeros(len(out))
    g1_pred = g1.predict(out[X]) if idx1.sum() > 0 else np.zeros(len(out))
    out["cate"] = e_test * g0_pred + (1.0 - e_test) * g1_pred
    return out


# --------------------------------------
# 4) Double ML (continuous treatment)
# --------------------------------------
def double_ml_cate(
    train: pd.DataFrame, test: pd.DataFrame, X: List[str], T: str, y: str
) -> pd.DataFrame:
    """
    Cross-fitted Double / Debiased ML for continuous T:

    1) Cross-fit m_y: E[Y|X], m_t: E[T|X] on train
    2) Residuals: Y_res = Y - m_y(X), T_res = T - m_t(X)
    3) Transformed outcome: Y* = Y_res / T_res  (epsilon guard)
       Weights: w = (T_res)^2
    4) Fit tau_model: X -> Y* with sample_weight=w
    Predict CATE on test as tau_model(X_test).
    """
    tr = train.copy()
    n = len(tr)

    kf = KFold(n_splits=2, shuffle=True, random_state=123)
    y_hat = np.zeros(n)
    t_hat = np.zeros(n)

    for tr_idx, val_idx in kf.split(tr):
        m_y = _gbdt()
        m_t = _gbdt()
        m_y.fit(tr.iloc[tr_idx][X], tr.iloc[tr_idx][y])
        m_t.fit(tr.iloc[tr_idx][X], tr.iloc[tr_idx][T])
        y_hat[val_idx] = m_y.predict(tr.iloc[val_idx][X])
        t_hat[val_idx] = m_t.predict(tr.iloc[val_idx][X])

    y_res = tr[y].to_numpy() - y_hat
    t_res = tr[T].to_numpy() - t_hat

    eps = 1e-6
    # guard division by ~0; if t_res==0, use +eps
    denom = np.where(np.abs(t_res) < eps, eps * (np.sign(t_res) + (t_res == 0)), t_res)
    y_star = y_res / denom
    w = t_res ** 2

    tau_model = _gbdt()
    tau_model.fit(tr[X], y_star, sample_weight=w)

    out = test.copy()
    out["cate"] = tau_model.predict(out[X])
    return out

