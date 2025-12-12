import numpy as np
import jax.numpy as jnp
import pyscsopt as scs
from pyscsopt.algorithms import ProxLQNSCORE, ProxGGNSCORE, ProxNSCORE
from pyscsopt.regularizers import PHuberSmootherGL
from pyscsopt.utils import make_group_lasso_problem

import jax
jax.config.update('jax_platform_name', 'cpu')
if not jax.config.jax_enable_x64:
    jax.config.update("jax_enable_x64", True)

np.random.seed(1234)

# generate synthetic group lasso regression data using utility
m = 50
n = 100
grpsize = 10
p_active = 0.1  # 10% of groups/features active
A, y, x_true, x0, groups, ind, P = make_group_lasso_problem(
    m=m, n=n, grpsize=grpsize, p_active=p_active, noise_std=0.1, seed=1234, group_weights=1.0, use_const_grpsize=True, corr=0.5)

# obj
# define the obj this way ONLY for ProxGGNSCORE (that is, allow for a precomputed yhat, in which case we don't need to provide all the gradient functions below)
def f(A, y, x, yhat=None):
    m = y.shape[0]
    if yhat is None:
        yhat = out_fn(A, x)
    return 0.5 * jnp.sum((yhat - y) ** 2)/m

# strictly OPTIONAL for all methods
def grad_fx(A, y, x):
    m = y.shape[0]
    return (A.T @ (A @ x - y))/m

# the following functions are used ONLY by ProxGGNSCORE (ONLY out_fn is required, others are optional as in other methods provided f is defined as above)
def out_fn(A, x):
    return A @ x

def jac_yx(A, y, yhat, x):
    return A

def grad_fy(A, y, yhat):
    m = y.shape[0]
    return (yhat - y)/m

def hess_fy(A, y, yhat):
    m = y.shape[0]
    return jnp.eye(len(yhat))/m

# regularization parameters
lam1 = 1e-8  # l1
lam2 = 1   # group lasso
lam = [lam1, lam2]
mu = 1e-2

x0 = np.random.randn(n)
reg_name = "gl"

# problem = scs.Problem(x0=x0, f=f, lam=lam, A=A, y=y, P=P, out_fn=out_fn, grad_fx=grad_fx, jac_yx=jac_yx, grad_fy=grad_fy, hess_fy=hess_fy)

# the following works fine (gradients are computed internally using jax)
problem = scs.Problem(x0=x0, f=f, lam=lam, A=A, y=y, P=P, out_fn=out_fn)

hmu = PHuberSmootherGL(mu, lam, P) # group lasso smoother takes also lam and P as input

method_lqn = ProxLQNSCORE(use_prox=True, ss_type=1, m=10)
sol_lqn = scs.iterate(method_lqn, problem, reg_name, hmu, verbose=1, max_epoch=100)

method_ggn = ProxGGNSCORE(use_prox=True, ss_type=1)
sol_ggn = scs.iterate(method_ggn, problem, reg_name, hmu, verbose=1, max_epoch=100)

hmu.mu = 1
method_n = ProxNSCORE(use_prox=True, ss_type=1)
sol_n = scs.iterate(method_n, problem, reg_name, hmu, verbose=1, max_epoch=100)

# ### uncomment to print solutions
# print("=" * 50)
# print("ProxLQNSCORE (Sparse Group Lasso):")
# print("Solution x:", sol_lqn.x)
# print("=" * 50)
# print("ProxGGNSCORE (Sparse Group Lasso):")
# print("Solution x:", sol_ggn.x)
# print("=" * 50)
# print("ProxNSCORE (Sparse Group Lasso):")
# print("Solution x:", sol_n.x)
