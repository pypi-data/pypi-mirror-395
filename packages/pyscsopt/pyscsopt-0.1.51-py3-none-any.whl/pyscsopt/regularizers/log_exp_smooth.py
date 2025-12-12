import numpy as np
from pyscsopt.utils.prox_reg_utils import bounds_sanity_check

def logexp_smooth2_indbox(x, mu=1.0, lb=0.0, ub=1.0):
    n = x.shape[0]
    a, b = bounds_sanity_check(n, lb, ub)
    out = np.zeros(n)
    for i in range(n):
        if x[i] <= a[i] + mu:
            out[i] += (a[i] - x[i] + 3*mu)*(a[i] - x[i] + mu)/(2*mu)
        elif x[i] >= b[i] - mu:
            out[i] += (x[i] - b[i] + 3*mu)*(x[i] - b[i] + mu)/(2*mu)
        if x[i] < a[i]:
            out[i] += mu * (np.log(mu) - np.log(x[i] - a[i]))
        elif x[i] > b[i]:
            out[i] += mu * (np.log(mu) - np.log(b[i] - x[i]))
    return out

def logexp_smooth2_grad_indbox(x, mu=1.0, lb=0.0, ub=1.0):
    n = x.shape[0]
    a, b = bounds_sanity_check(n, lb, ub)
    out = np.zeros(n)
    for i in range(n):
        if x[i] <= a[i] + mu:
            out[i] += (x[i] - a[i] - 2*mu)/mu
        elif x[i] >= b[i] - mu:
            out[i] += (x[i] - b[i] + 2*mu)/mu
        if x[i] < a[i]:
            out[i] += mu/(a[i] - x[i])
        elif x[i] > b[i]:
            out[i] += -mu/(b[i] - x[i])
    return out

def logexp_smooth2_hess_indbox(x, mu=1.0, lb=0.0, ub=1.0):
    n = x.shape[0]
    a, b = bounds_sanity_check(n, lb, ub)
    out = np.zeros(n)
    for i in range(n):
        if x[i] <= a[i] + mu:
            out[i] += 1/mu
        elif x[i] >= b[i] - mu:
            out[i] += 1/mu
        if x[i] < a[i]:
            out[i] += mu/(a[i] - x[i])**2
        elif x[i] > b[i]:
            out[i] += mu/(b[i] - x[i])**2
    return out

class LogExpSmootherIndBox:
    def __init__(self, C_set, mu):
        self.mu = mu
        self.lb = C_set[0]
        self.ub = C_set[1]
        self.Mh = 1.0
        self.nu = 2.0
    def val(self, x):
        return logexp_smooth2_indbox(x, self.mu, self.lb, self.ub)
    def grad(self, Cmat, x):
        return logexp_smooth2_grad_indbox(x, self.mu, self.lb, self.ub)
    def hess(self, Cmat, x):
        return logexp_smooth2_hess_indbox(x, self.mu, self.lb, self.ub)