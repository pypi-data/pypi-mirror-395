import numpy as np
import pyscsopt as scs
from pyscsopt.regularizers import LogExpSmootherIndBox
from pyscsopt.algorithms import ProxLQNSCORE

import numpy as np
import jax.numpy as jnp
import jax.random as random

import jax
jax.config.update('jax_platform_name', 'cpu')
if not jax.config.jax_enable_x64:
    jax.config.update("jax_enable_x64", True)

np.random.seed(1234)

nvar = 10
Q = jnp.tril(random.uniform(random.PRNGKey(1234), (nvar, nvar)))
Q = Q + Q.T - jnp.diag(Q.diagonal())
Q = Q + nvar * jnp.eye(nvar)
c = jnp.ones(nvar)

def f(x):
    return 0.5 * jnp.dot(x, jnp.dot(Q, x)) + jnp.dot(c, x)

x0 = random.uniform(random.PRNGKey(1111), (nvar,))
lbda = 1.0
reg_name = "indbox"
mu = 1e-2
C_set = (-1.0, 1.0)
hmu = LogExpSmootherIndBox(C_set, mu)
problem = scs.Problem(x0, f, lbda, C_set=C_set)

method_lqn = ProxLQNSCORE(use_prox=True, ss_type=1, m=10)
sol_lqn = scs.iterate(method_lqn, problem, reg_name, hmu, verbose=1, max_epoch=200)

# ### uncomment to print solutions
# print("=" * 50)
# print("ProxLQNSCORE:")
# print("Solution x:", sol_lqn.x)