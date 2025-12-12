import numpy as np
import jax.numpy as jnp
import pyscsopt as scs
from pyscsopt.algorithms import ProxLQNSCORE, ProxNSCORE, ProxGGNSCORE
from pyscsopt.regularizers import PHuberSmootherL1L2

import jax
jax.config.update('jax_platform_name', 'cpu')
if not jax.config.jax_enable_x64:
    jax.config.update("jax_enable_x64", True)

np.random.seed(1234)

# Data dimensions
m, n = 50, 100
A = np.random.randn(m, n) * (np.random.rand(m, n) < 1e-2)
x0 = np.random.randn(n)

# true solution (sparse x_true)
x_true = np.zeros(n)
num_nonzero = max(1, n//10)
nonzero_idx = np.random.choice(n, size=num_nonzero, replace=False)
x_true[nonzero_idx] = np.random.randn(num_nonzero)

# generate labels
y_prob = 1 / (1 + jnp.exp(-A @ x_true))
y = np.random.binomial(1, y_prob)
unique_y = np.unique(y)
y = np.where(y == unique_y[0], -1, 1)

# obj
# define the obj this way ONLY for ProxGGNSCORE (that is, allow for a precomputed yhat, in which case we don't need to provide all the gradient functions below)
def f(A, y, x, yhat=None):
    m = y.shape[0]
    if yhat is None:
        yhat = out_fn(A, x)
    logit_yhat = jnp.log(yhat / (1 - yhat))
    return 1/m * jnp.sum(jnp.log(1 + jnp.exp(-y * logit_yhat)))

# the following functions are used ONLY by ProxGGNSCORE (ONLY out_fn is required, others are optional as in other methods provided f is defined as above)
def out_fn(A, x):
    return 1 / (1 + jnp.exp(-A @ x))

def grad_fx(A, y, x):
    Sx = jnp.exp(-y * (A @ x))
    return -A.T @ (y * (Sx / (1 + Sx))) / m

def hess_fx(A, y, x):
    Sx = 1 / (1 + jnp.exp(-y * (A @ x)))
    W = jnp.diag(Sx * (1 - Sx))
    return A.T @ W @ A / m

def jac_yx(A, y, yhat, x):
    return (yhat * (1 - yhat))[:, None] * A

def grad_fy(A, y, yhat):
    return (-y / yhat + (1 - y) / (1 - yhat)) / m

def hess_fy(A, y, yhat):
    return jnp.diag((y / yhat**2 + (1 - y) / (1 - yhat)**2) / m)

reg_name = "l1"
lbda = 1e-1
mu = 1
hmu = PHuberSmootherL1L2(mu)

# problem = scs.Problem(x0=x0, f=f, lam=lbda, A=A, y=y, out_fn=out_fn, grad_fx=grad_fx, jac_yx=jac_yx, grad_fy=grad_fy, hess_fy=hess_fy)

# the following works fine (gradients are computed internally using jax)
problem = scs.Problem(x0=x0, f=f, lam=lbda, A=A, y=y, out_fn=out_fn)

method_lqn = ProxLQNSCORE(use_prox=True, ss_type=1, m=10)
sol_lqn = scs.iterate(method_lqn, problem, reg_name, hmu, verbose=1, max_epoch=100)

method_nscore = ProxNSCORE(use_prox=True, ss_type=1)
sol_nscore = scs.iterate(method_nscore, problem, reg_name, hmu, max_epoch=100, x_tol=1e-6, f_tol=1e-6, verbose=1)

method_ggn = ProxGGNSCORE(use_prox=True, ss_type=1)
sol_ggn = scs.iterate(method_ggn, problem, reg_name, hmu, max_epoch=100, x_tol=1e-6, f_tol=1e-6, verbose=1)

# ### uncomment to print solutions
# print("=" * 50)
# print("ProxLQNSCORE (Sparse Logistic Regression):")
# print("Solution x:", sol_lqn.x)
# print("=" * 50)
# print("ProxNSCORE (Sparse Logistic Regression):")
# print("Solution x:", sol_nscore.x)
# print("=" * 50)
# print("ProxGGNSCORE (Sparse Logistic Regression):")
# print("Solution x:", sol_ggn.x)
