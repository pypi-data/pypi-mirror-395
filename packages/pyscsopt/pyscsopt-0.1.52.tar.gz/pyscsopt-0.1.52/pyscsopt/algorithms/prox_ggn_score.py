import numpy as np
import jax
import jax.numpy as jnp
from pyscsopt.utils.utils import linesearch, inv_BB_step
from pyscsopt.regularizers.smoothing import get_Mg
import pyscsopt.prox.prox_operators as prox_ops

class ProxGGNSCORE:
    def __init__(self, ss_type=1, use_prox=True, name="prox-ggnscore", label="Prox-GGN-SCORE"):
        self.ss_type = ss_type
        self.use_prox = use_prox
        self.name = name
        self.label = label

    def init(self, x):
        return self

    def ggn_score_step(self, J, Q, gr, Hr_diag, H_inv, residual, lam):
        # gr: list of gradient vectors (each (n,)), or a single (n,) vector
        ncat = len(gr) if isinstance(gr, list) else 1
        n = gr[0].shape[0] if isinstance(gr, list) else gr.shape[0]
        # stack gradients as columns
        if ncat > 1:
            gr_mat = jnp.column_stack([jnp.asarray(g).reshape(-1) for g in gr])  # (n, ncat)
        else:
            gr_mat = jnp.asarray(gr).reshape(n, 1)  # (n, 1)
        # Jt: [J.T  λ*gr_mat]
        Jt = jnp.hstack([J.T, lam * gr_mat])  # (n, m+ncat)
        # residual: [residual ; ones(ncat)]
        residual_vec = jnp.concatenate([residual, jnp.ones(ncat)])
        # Q_aug: block matrix
        qdm1 = Q.shape[0]
        qdm11 = qdm1 + ncat
        Q_aug = np.zeros((qdm11, qdm11))
        Q_aug[:qdm1, :qdm1] = Q
        # the rest is zeros
        if qdm11 <= n:
            A = Q_aug @ (Jt.T @ H_inv) @ Jt
            B = jnp.linalg.solve(ncat*jnp.eye(qdm11) + A, residual_vec)
            d = H_inv @ Jt @ B
        else:
            JQJ = (Jt @ Q_aug @ Jt.T) + lam * jnp.diag(Hr_diag)
            Je = Jt @ residual_vec
            JQJ_qr = jnp.linalg.qr(JQJ)
            JQJ_q, JQJ_r = JQJ_qr[0], JQJ_qr[1]
            d = jnp.linalg.solve(JQJ_r, JQJ_q.T @ Je)
        return -d

    def step(self, model, reg_name, hmu, As, x, x_prev, ys, Cmat, iter):
        lam = model.lam[0] if hasattr(model.lam, '__len__') and len(model.lam) > 1 else model.lam
        gr = hmu.grad(Cmat, x)
        lam_gr = lam * gr
        Hr_diag = hmu.hess(Cmat, x)
        if all([getattr(model, attr, None) is not None for attr in ("jac_yx", "grad_fy", "hess_fy")]):
            yhat = model.out_fn(As, x)
            J = model.jac_yx(As, ys, yhat, x)
            residual = model.grad_fy(As, ys, yhat)
            Q = model.hess_fy(As, ys, yhat)
        else:
            m_out_fn = lambda z: model.out_fn(As, z)
            yhat = m_out_fn(x)
            f = lambda y_: model.f(As, ys, x, yhat=y_)
            J = jax.jacobian(m_out_fn)(x)
            residual = jax.grad(f)(yhat)
            Q = jax.hessian(f)(yhat)
        if hasattr(model, 'grad_fx') and model.grad_fx is not None:
            grad_f = lambda x_: model.grad_fx(As, ys, x_)
        else:
            grad_f = lambda x_: jnp.array(jax.grad(lambda z: model.f(As, ys, z))(x_))
        Hdiag_inv = 1.0 / Hr_diag
        H_inv = jnp.diag(Hdiag_inv)
        d = self.ggn_score_step(J, Q, [gr], Hr_diag, H_inv, residual, lam)
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
                grad_curr = grad_f(x) + lam_gr
                step_size = inv_BB_step(x, x_prev, grad_curr, grad_prev)
        elif self.ss_type == 3:
            step_size = linesearch(x, d, lambda z: model.f(As, ys, z) + model.get_reg(z, reg_name), grad_f)
        else:
            raise ValueError("Please, choose ss_type in [1, 2, 3].")
        Mg = get_Mg(hmu.Mh, hmu.nu, hmu.mu, len(x))
        eta = jnp.sqrt(jnp.dot(lam_gr, H_inv @ lam_gr))
        alpha = step_size / (1 + Mg * eta)
        safe_alpha = min(1, alpha)
        if self.use_prox:
            x_new = prox_ops.invoke_prox(model, reg_name, x + safe_alpha * d, Hdiag_inv, lam, step_size)
        else:
            x_new = x + safe_alpha * d
        return x_new, jnp.linalg.norm(x_new - x)
