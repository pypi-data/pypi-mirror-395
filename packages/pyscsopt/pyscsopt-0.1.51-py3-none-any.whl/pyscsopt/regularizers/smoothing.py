import numpy as np

class NoSmooth:
    def __init__(self, mu):
        self.mu = mu
    def val(self, x):
        return np.zeros_like(x)
    def grad(self, x):
        return np.zeros_like(x)
    def hess(self, x):
        return np.finfo(float).eps * np.ones_like(x)

def get_Mg(Mh, nu, mu, n):
    if Mh < 0:
        raise ValueError("Mh must be nonnegative.")
    if mu <= 0:
        raise ValueError("mu must be positive.")
    if 0 < nu <= 3:
        return n ** ((3 - nu) / 2) * mu ** (nu / 2 - 2) * Mh
    elif nu > 3:
        return mu ** (4 - 3 * nu / 2) * Mh
    else:
        raise ValueError("nu must be positive.")