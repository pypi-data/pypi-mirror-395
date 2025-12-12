import numpy as np
import pyscsopt as scs
from pyscsopt.regularizers import PHuberSmootherL1L2
from pyscsopt.algorithms import ProxLQNSCORE

import jax
jax.config.update('jax_platform_name', 'cpu')
if not jax.config.jax_enable_x64:
    jax.config.update("jax_enable_x64", True)

import numpy as np
import jax.numpy as jnp

np.random.seed(1234)

def f(x):
    return 100 * (x[1] - x[0]**2)**2 + (1 - x[0])**2

x0 = jnp.array([0.0, 0.0])
lbda = 1e-8 # or set to zero to remove regularization entirely
reg_name = "l1" # see other examples for other regularization names
mu = 1e-2
hmu = PHuberSmootherL1L2(mu)
problem = scs.Problem(x0, f, lbda)

# proximal LQNSCORE (L-BFGS-SCORE)
method_lqn = ProxLQNSCORE(use_prox=True, ss_type=1, m=10)
sol_lqn = scs.iterate(method_lqn, problem, reg_name, hmu, verbose=1, max_epoch=100)

# ### uncomment to print solutions
# print("=" * 50)
# print("ProxLQNSCORE:")
# print("Solution x:", sol_lqn.x)