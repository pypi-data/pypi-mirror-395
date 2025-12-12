import numpy as np
from pyscsopt.utils.prox_reg_utils import bounds_sanity_check

def exp_smooth_indbox(x, mu=1.0, lb=0.0, ub=1.0):
    n = x.shape[0]
    a, b = bounds_sanity_check(n, lb, ub)
    return np.exp((-x + a) / mu) * mu

def exp_smooth_grad_indbox(x, mu=1.0, lb=0.0, ub=1.0):
    n = x.shape[0]
    a, b = bounds_sanity_check(n, lb, ub)
    return -np.exp((-x + a) / mu)

def exp_smooth_hess_indbox(x, mu=1.0, lb=0.0, ub=1.0):
    n = x.shape[0]
    a, b = bounds_sanity_check(n, lb, ub)
    return (1 / mu) * np.exp((-x + a) / mu)

class ExponentialSmootherIndBox:
    def __init__(self, C_set, mu):
        self.mu = mu
        self.lb = C_set[0]
        self.ub = C_set[1]
        self.Mh = 1.0
        self.nu = 2.0
    def val(self, x):
        return exp_smooth_indbox(x, self.mu, self.lb, self.ub)
    def grad(self, Cmat, x):
        return exp_smooth_grad_indbox(x, self.mu, self.lb, self.ub)
    def hess(self, Cmat, x):
        return exp_smooth_hess_indbox(x, self.mu, self.lb, self.ub)