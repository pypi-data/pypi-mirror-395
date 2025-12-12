import numpy as np
import jax.numpy as jnp
import pytest
from pyscsopt.problems import Problem
from pyscsopt.algorithms.prox_n_score import ProxNSCORE
from pyscsopt.algorithms.prox_ggn_score import ProxGGNSCORE
from pyscsopt.regularizers.phuber_smooth import PHuberSmootherL1L2, PHuberSmootherIndBox
from pyscsopt.regularizers.exponential_smooth import ExponentialSmootherIndBox
from pyscsopt.algorithms.iterate import iterate

TOL = 1e-4

@pytest.mark.parametrize("reg_name", ["l1", "l2"])
def test_proximal_newton_score_regression(reg_name):
    A = jnp.array([[-0.560501, 0.0], [0.0, 1.85278], [-0.0192918, -0.827763], [0.128064, 0.110096], [0.0, -0.251176]])
    y = jnp.array([-1, -1, -1, 1, -1])
    x0 = jnp.array([0.5908446386657102, 0.7667970365022592])
    lam = 1e-2
    mu = 0.5
    def f_reg(A, y, x):
        return 1/5 * jnp.sum(jnp.log(1 + jnp.exp(-y * (A @ x))))
    model = Problem(x0=x0, f=f_reg, lam=lam, A=A, y=y)
    hmu = PHuberSmootherL1L2(mu)
    sol = iterate(ProxNSCORE(), model, reg_name, hmu, max_epoch=50)
    assert sol.epochs+1 >= 1
    # assert sol.rel[-1] <= TOL
    assert sol.objrel[-1] <= TOL

@pytest.mark.parametrize("reg_name", ["l1", "l2"])
def test_proximal_ggn_score_regression(reg_name):
    A = jnp.array([[-0.560501, 0.0], [0.0, 1.85278], [-0.0192918, -0.827763], [0.128064, 0.110096], [0.0, -0.251176]])
    y = jnp.array([-1, -1, -1, 1, -1])
    x0 = jnp.array([0.5908446386657102, 0.7667970365022592])
    lam = 1e-2
    mu = 0.5
    def f_reg(A, y, x, yhat=None):
        m = y.shape[0]
        if yhat is None:
            yhat = Mfunc(A, x)
        logit_yhat = jnp.log(yhat / (1 - yhat))
        return 1/m * jnp.sum(jnp.log(1 + jnp.exp(-y * logit_yhat)))
    def Mfunc(A, x):
        return 1 / (1 + jnp.exp(-A @ x))
    model = Problem(x0=x0, f=f_reg, lam=lam, A=A, y=y, out_fn=Mfunc)
    hmu = PHuberSmootherL1L2(mu)
    sol = iterate(ProxGGNSCORE(), model, reg_name, hmu, max_epoch=50)
    assert sol.epochs+1 >= 1
    # assert sol.rel[-1] <= TOL
    assert sol.objrel[-1] <= TOL

def test_phuber_and_exp_indbox():
    A = jnp.array([
        [1.53976, 0.201833, 0.433995, 0.156497, 0.180124],
        [0.201833, 2.37257, -0.0594941, -0.671533, 0.0739676],
        [0.433995, -0.0594941, 3.15025, 0.808797, 0.954656],
        [0.156497, -0.671533, 0.808797, 2.74361, 0.5621],
        [0.180124, 0.0739676, 0.954656, 0.5621, 1.76141]
    ])
    y = jnp.array([0.8673472019512456, -0.9017438158568171, -0.4944787535042339, -0.9029142938652416, 0.8644013132535154])
    x0 = jnp.array([-2.07754990163271, -2.311005948690538, -0.25157276401631606, -0.8858618022602884, 1.3116613046047525])
    x_star = jnp.array([-0.7139006111210786, 0.642716661564418, 0.3684773651494535, 0.5890487798472874, -0.8324174178513779])
    lam = 1.0e-4
    mu = 0.6
    lb = -1.0
    ub = 1.0
    def f_qp(A, y, x):
        return 0.5 * x @ (A @ x) + y @ x
    model_phuber = Problem(x0=x0, f=f_qp, lam=lam, A=A, y=y, C_set=[lb, ub], x=x_star)
    hmu_phuber = PHuberSmootherIndBox(lb, ub, mu)
    sol_p = iterate(ProxNSCORE(), model_phuber, "indbox", hmu_phuber, max_epoch=50, alpha=0.8)
    assert sol_p.epochs+1 >= 1
    # assert sol_p.rel[-1] <= 1e-3
    assert sol_p.objrel[-1] <= 1e-3
    model_exp = Problem(x0=x0, f=f_qp, lam=lam, A=A, y=y, C_set=[lb, ub], x=x_star)
    hmu_exp = ExponentialSmootherIndBox((lb, ub), mu)
    sol_e = iterate(ProxNSCORE(), model_exp, "indbox", hmu_exp, max_epoch=50, alpha=1.0)
    assert sol_e.epochs+1 >= 1
    # assert sol_e.rel[-1] <= 1e-3
    assert sol_e.objrel[-1] <= 1e-3
