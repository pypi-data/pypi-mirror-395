import numpy as np
import jax
import jax.numpy as jnp
from pyscsopt.utils.utils import linesearch, inv_BB_step
from pyscsopt.regularizers.smoothing import get_Mg
import pyscsopt.prox.prox_operators as prox_ops

class ProxNSCORE:
    def __init__(self, ss_type=1, use_prox=True, name="prox-newtonscore", label="Prox-N-SCORE"):
        self.ss_type = ss_type
        self.use_prox = use_prox
        self.name = name
        self.label = label

    def init(self, x):
        return self

    def step(self, model, reg_name, hmu, As, x, x_prev, ys, Cmat, iter):
        lam = model.lam[0] if hasattr(model.lam, '__len__') and len(model.lam) > 1 else model.lam
        gr = hmu.grad(Cmat, x)
        lam_gr = lam * gr
        Hr_diag = hmu.hess(Cmat, x)
        is_generic = (model.A is None or model.y is None)
        if is_generic:
            obj = lambda x_: model.f(x_)
            if hasattr(model, 'grad_fx') and model.grad_fx is not None and hasattr(model, 'hess_fx') and model.hess_fx is not None:
                H = model.hess_fx(x)
                grad_f = lambda x_: model.grad_fx(x_)
            else:
                H = jnp.array(jax.hessian(obj)(x))
                grad_f = lambda x_: jnp.array(jax.grad(obj)(x_))
        else:
            obj = lambda x_: model.f(As, ys, x_)
            if hasattr(model, 'grad_fx') and model.grad_fx is not None and hasattr(model, 'hess_fx') and model.hess_fx is not None:
                H = model.hess_fx(As, ys, x)
                grad_f = lambda x_: model.grad_fx(As, ys, x_)
            else:
                H = jnp.array(jax.hessian(obj)(x))
                grad_f = lambda x_: jnp.array(jax.grad(obj)(x_))
        lam_Hr = lam * jnp.diag(Hr_diag)
        grad = grad_f(x) + lam_gr
        d = -jnp.linalg.solve(H + lam_Hr, grad)
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
        H_inv = jnp.diag(Hdiag_inv)
        Mg = get_Mg(hmu.Mh, hmu.nu, hmu.mu, len(x))
        d_norm = jnp.dot(lam_gr, jnp.dot(H_inv, lam_gr))
        eta = jnp.sqrt(d_norm)
        alpha = step_size / (1 + Mg * eta)
        safe_alpha = min(1, alpha)
        if self.use_prox:
            x_new = prox_ops.invoke_prox(model, reg_name, x + safe_alpha * d, Hdiag_inv, lam, step_size)
        else:
            x_new = x + safe_alpha * d
        return x_new, jnp.linalg.norm(x_new - x)