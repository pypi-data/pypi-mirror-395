
import numpy as np, pandas as pd
from patsy import dmatrix
from sklearn.linear_model import LogisticRegression, LinearRegression

EPS = 1e-6
def _X(df, formula): return np.asarray(dmatrix(formula, df, return_type="dataframe"))

def ipw(df, ps_formula, T, Y):
    t = df[T].to_numpy(dtype=float); y = df[Y].to_numpy(dtype=float); X = _X(df, ps_formula)
    lr = LogisticRegression(penalty=None, max_iter=1000).fit(X, t)
    e = np.clip(lr.predict_proba(X)[:,1], EPS, 1-EPS)
    return float(np.mean((t - e)/(e*(1-e))*y))

def doubly_robust(df, formula, T, Y):
    t = df[T].to_numpy(dtype=float); y = df[Y].to_numpy(dtype=float); X = _X(df, formula)
    lr = LogisticRegression(penalty=None, max_iter=1000).fit(X, t)
    e = np.clip(lr.predict_proba(X)[:,1], EPS, 1-EPS)
    X1, y1 = X[t==1], y[t==1]; X0, y0 = X[t==0], y[t==0]
    mu1 = LinearRegression().fit(X1, y1).predict(X)
    mu0 = LinearRegression().fit(X0, y0).predict(X)
    term1 = t*(y - mu1)/e + mu1; term0 = (1-t)*(y - mu0)/(1-e) + mu0
    return float(np.mean(term1 - term0))

