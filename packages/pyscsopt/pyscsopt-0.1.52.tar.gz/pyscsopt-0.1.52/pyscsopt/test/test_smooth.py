import numpy as np
import pytest
from pyscsopt.regularizers.phuber_smooth import PHuberSmootherL1L2, PHuberSmootherIndBox, PHuberSmootherGL
from pyscsopt.regularizers.log_exp_smooth import LogExpSmootherIndBox
from pyscsopt.regularizers.exponential_smooth import ExponentialSmootherIndBox

mu = 1
lb = -1.0
ub = 1.0

def test_phuber_l1l2():
    hmu = PHuberSmootherL1L2(mu)
    assert hmu.Mh == 2.0
    assert hmu.nu == 2.6

def test_phuber_indbox():
    hmu = PHuberSmootherIndBox(lb, ub, mu)
    assert hmu.Mh == 2.0
    assert hmu.nu == 2.6

def test_phuber_group_lasso():
    # minimal mock for group lasso model
    class P:
        def __init__(self):
            self.ind = [0, 1]
            self.grpNUM = 1
            self.tau = 0.9
    lam = [0.09, 0.91]
    P = P()
    hmu = PHuberSmootherGL(mu, lam, P)
    assert hmu.Mh == 2.0
    assert hmu.nu == 2.6

def test_logexp_smoother_indbox():
    C_set = [lb, ub]
    hmu = LogExpSmootherIndBox(C_set, mu)
    assert hmu.Mh == 1.0
    assert hmu.nu == 2.0

def test_exponential_smoother_indbox():
    C_set = [lb, ub]
    hmu = ExponentialSmootherIndBox(C_set, mu)
    assert hmu.Mh == 1.0
    assert hmu.nu == 2.0
