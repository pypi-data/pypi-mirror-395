import numpy as np
import jax
import jax.numpy as jnp
from pyscsopt.utils.utils import linesearch, inv_BB_step
from pyscsopt.regularizers.smoothing import get_Mg
import pyscsopt.prox.prox_operators as prox_ops

class ProxLQNSCORE:
    def __init__(self, ss_type=1, use_prox=True, name="prox-lbfgsscore", label="Prox-LBFGS-SCORE", m=10):
        self.ss_type = ss_type
        self.use_prox = use_prox
        self.name = name
        self.label = label
        self.m = m  # memory size
        self.s_list = []  # s = x_{k+1} - x_k
        self.y_list = []  # y = grad_{k+1} - grad_k
        self.H0 = None  # initial Hessian scaling (scalar or identity)

    def init(self, x):
        n = x.shape[0]
        self.s_list = []
        self.y_list = []
        self.H0 = jnp.eye(n)
        return self

    def two_loop_recursion(self, grad):
        q = grad.copy()
        alpha = []
        rho = []
        for s, y in zip(reversed(self.s_list), reversed(self.y_list)):
            rho_i = 1.0 / jnp.dot(y, s)
            alpha_i = rho_i * jnp.dot(s, q)
            q = q - alpha_i * y
            alpha.append(alpha_i)
            rho.append(rho_i)
        r = self.H0 @ q
        for i in range(len(self.s_list)):
            s = self.s_list[i]
            y = self.y_list[i]
            rho_i = rho[-(i+1)]
            alpha_i = alpha[-(i+1)]
            beta = rho_i * jnp.dot(y, r)
            r = r + s * (alpha_i - beta)
        return -r

    def step(self, model, reg_name, hmu, As, x, x_prev, ys, Cmat, iter):
        lam = model.lam[0] if hasattr(model.lam, '__len__') and len(model.lam) > 1 else model.lam
        gr = hmu.grad(Cmat, x)
        lam_gr = lam * gr
        Hr_diag = hmu.hess(Cmat, x)
        is_generic = (model.A is None or model.y is None)
        if is_generic:
            obj = lambda x_: model.f(x_) + model.get_reg(x_, reg_name)
            grad_f = model.grad_fx if hasattr(model, 'grad_fx') and model.grad_fx is not None else lambda x_: jnp.array(jax.grad(obj)(x_))
        else:
            obj = lambda x_: model.f(As, ys, x_) + model.get_reg(x_, reg_name)
            if hasattr(model, 'grad_fx') and model.grad_fx is not None:
                grad_f = lambda x_: model.grad_fx(As, ys, x_)
            else:
                grad_f = lambda x_: jnp.array(jax.grad(lambda z: model.f(As, ys, z))(x_))
        grad = grad_f(x) + lam_gr
        if iter == 0 or len(self.s_list) == 0:
            d = -grad
        else:
            d = self.two_loop_recursion(grad)
        if self.ss_type == 1 and getattr(model, 'L', None) is not None:
            step_size = min(1.0 / model.L, 1.0)
        elif self.ss_type == 1 and getattr(model, 'L', None) is None:
            step_size = 0.5
        elif self.ss_type == 2:
            if iter == 1:
                step_size = 1.0
            else:
                lam_gr_prev = lam * hmu.grad(Cmat, x_prev)
                grad_prev = grad_f(x_prev) + lam_gr_prev
                step_size = inv_BB_step(x, x_prev, grad, grad_prev)
        elif self.ss_type == 3:
            step_size = linesearch(x, d, obj, grad_f)
        else:
            raise ValueError("Please, choose ss_type in [1, 2, 3].")
        Hdiag_inv = 1.0 / Hr_diag
        Mg = get_Mg(hmu.Mh, hmu.nu, hmu.mu, len(x))
        eta = jnp.sqrt(jnp.dot(lam_gr, lam_gr * Hdiag_inv))
        alpha = step_size / (1 + Mg * eta)
        safe_alpha = min(1, alpha)
        if self.use_prox:
            x_new = prox_ops.invoke_prox(model, reg_name, x + safe_alpha * d, Hdiag_inv, lam, step_size)
        else:
            x_new = x + safe_alpha * d
        grad_fxnew = grad_f(x_new)
        grad_new = grad_fxnew + lam * hmu.grad(Cmat, x_new)
        s = x_new - x
        y = grad_new - grad
        if jnp.dot(s, y) > 1e-10:
            if len(self.s_list) == self.m:
                self.s_list.pop(0)
                self.y_list.pop(0)
            self.s_list.append(s)
            self.y_list.append(y)
            self.H0 = (jnp.dot(y, s) / jnp.dot(y, y)) * jnp.eye(len(x))
        return x_new, jnp.linalg.norm(x_new - x)
