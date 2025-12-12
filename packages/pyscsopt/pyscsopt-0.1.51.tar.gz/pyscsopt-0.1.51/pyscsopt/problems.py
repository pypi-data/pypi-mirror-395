import numpy as np
import jax
from pyscsopt.regularizers.regularizers import get_reg

class Problem:
    def __init__(self, x0, f, lam, L=None, x=None, C_set=None, P=None, re=None, grad_fx=None, hess_fx=None, jac_yx=None, grad_fy=None, hess_fy=None, name=None, A=None, y=None, out_fn=None):
        self.x0 = x0
        self.f = f
        self.lam = lam
        self.L = L
        self.x = x if x is not None else np.zeros_like(x0)
        self.C_set = C_set
        self.P = P
        self.re = re
        self.grad_fx = grad_fx
        self.hess_fx = hess_fx
        self.jac_yx = jac_yx
        self.grad_fy = grad_fy
        self.hess_fy = hess_fy
        self.name = name
        self.A = A
        self.y = y
        self.out_fn = out_fn

    def get_reg(self, x, reg_name):
        return get_reg(self, x, reg_name)