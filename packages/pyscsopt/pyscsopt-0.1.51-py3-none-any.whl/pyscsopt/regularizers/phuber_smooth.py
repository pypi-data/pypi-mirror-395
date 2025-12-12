import numpy as np
from pyscsopt.utils.prox_reg_utils import bounds_sanity_check

def pseudo_huber(x, mu=1.0):
    return (mu**2 - mu * np.sqrt(mu**2 + x**2) + x**2) / np.sqrt(mu**2 + x**2)

def huber_grad(x, mu=1.0):
    return x / np.sqrt(mu**2 + x**2)

def huber_hess(x, mu=1.0):
    return mu**2/(mu**2 + x**2)**(3/2)

def pseudo_huber_indbox(x, mu=1.0, lb=0.0, ub=1.0):
    n = x.shape[0]
    h = np.zeros(n)
    a, b = bounds_sanity_check(n, lb, ub)
    for i in range(n):
        if x[i] < a[i]:
            h[i] = (-mu * np.sqrt(a[i]**2 - 2*a[i]*x[i] + mu**2 + x[i]**2) + mu**2 + (-x[i] + a[i])**2) / np.sqrt(a[i]**2 - 2*a[i]*x[i] + mu**2 + x[i]**2)
        elif x[i] == a[i] or x[i] <= b[i]:
            h[i] = np.finfo(float).eps
        else:
            h[i] = (-mu * np.sqrt(b[i]**2 - 2*b[i]*x[i] + mu**2 + x[i]**2) + mu**2 + (b[i] - x[i])**2) / np.sqrt(b[i]**2 - 2*b[i]*x[i] + mu**2 + x[i]**2)
    return h

def huber_grad_indbox(x, mu=1.0, lb=0.0, ub=1.0):
    n = x.shape[0]
    g = np.zeros(n)
    a, b = bounds_sanity_check(n, lb, ub)
    for i in range(n):
        if -x[i] < a[i]:
            g[i] = ((a[i]**2 - 2*x[i]*a[i] + mu**2 + x[i]**2)**(-0.5)) * (-x[i] + a[i])
        elif x[i] == a[i] or x[i] < b[i]:
            g[i] = np.finfo(float).eps
        else:
            g[i] = ((b[i]**2 - 2*b[i]*x[i] + mu**2 + x[i]**2)**(-0.5)) * (b[i] - x[i])
    return g

def huber_hess_indbox(x, mu=1.0, lb=0.0, ub=1.0):
    n = x.shape[0]
    h = np.zeros(n)
    a, b = bounds_sanity_check(n, lb, ub)
    for i in range(n):
        if x[i] <= a[i]:
            h[i] = mu**2 * (a[i]**2 - 2*a[i]*x[i] + mu**2 + x[i]**2)**(-1.5)
        elif a[i] < x[i] < b[i]:
            h[i] = np.finfo(float).eps
        elif x[i] >= b[i]:
            h[i] = mu**2 * (b[i]**2 - 2*b[i]*x[i] + mu**2 + x[i]**2)**(-1.5)
    return h

def twonorm(x, kstart, kend):
    return np.linalg.norm(x[kstart:kend+1])

def infconv_huber_norm(x, lam, inds, grpNUM, mu):
    ICz = np.copy(x)
    ind = np.concatenate(inds)
    for j in range(grpNUM):
        lamw = lam * ind[2+3*j]
        kstart = int(ind[3*j])
        kend = int(ind[1+3*j])
        nrm = twonorm(x, kstart, kend)
        for k in range(kstart, kend+1):
            ICz[k] = x[k] * max(1 - lamw / nrm, 0)
            ICz[k] = pseudo_huber(ICz[k], mu)
    return ICz

def get_infconv_huber_l2l1(x, lam1, lam2, inds, grpNUM, mu):
    utmp = infconv_huber_norm(x, lam1, inds, grpNUM, mu)
    z = infconv_huber_norm(utmp, lam2, inds, grpNUM, mu)
    return z

def huber_l2l1_grad(Cmat, x, lam1, lam2, inds, grpNUM, mu):
    g_mu1 = pseudo_huber(x, mu)
    Dg_mu1 = huber_grad(x, mu)
    return huber_grad(np.dot(Cmat, g_mu1), mu) * Dg_mu1

def huber_l2l1_hess(Cmat, x, lam1, lam2, inds, grpNUM, mu):
    g_mu1 = pseudo_huber(x, mu)
    Dg_mu1 = huber_grad(x, mu)
    DDg_mu1 = huber_hess(x, mu)
    DDgg = huber_hess(np.dot(Cmat, g_mu1), mu) * np.dot(Dg_mu1, Dg_mu1) + huber_grad(np.dot(Cmat, g_mu1), mu) * DDg_mu1
    return DDgg

class PHuberSmootherL1L2:
    def __init__(self, mu):
        self.mu = mu
        self.Mh = 2.0
        self.nu = 2.6
    def val(self, x):
        return pseudo_huber(x, self.mu)
    def grad(self, Cmat, x):
        return huber_grad(x, self.mu)
    def hess(self, Cmat, x):
        return huber_hess(x, self.mu)

class PHuberSmootherIndBox:
    def __init__(self, lb, ub, mu):
        self.mu = mu
        self.lb = lb
        self.ub = ub
        self.Mh = 2.0
        self.nu = 2.6
    def val(self, x):
        return pseudo_huber_indbox(x, self.mu, self.lb, self.ub)
    def grad(self, Cmat, x):
        return huber_grad_indbox(x, self.mu, self.lb, self.ub)
    def hess(self, Cmat, x):
        return huber_hess_indbox(x, self.mu, self.lb, self.ub)

class PHuberSmootherGL:
    def __init__(self, mu, lam, P):
        self.mu = mu
        self.Mh = 2.0
        self.nu = 2.6
        inds = P.ind
        grpNUM = P.grpNUM
        self.lam1 = lam[0]
        self.lam2 = lam[1]
        self.inds = inds
        self.grpNUM = grpNUM
    def val(self, x):
        return get_infconv_huber_l2l1(x, self.lam1, self.lam2, self.inds, self.grpNUM, self.mu)
    def grad(self, Cmat, x):
        return huber_l2l1_grad(Cmat, x, self.lam1, self.lam2, self.inds, self.grpNUM, self.mu)
    def hess(self, Cmat, x):
        return huber_l2l1_hess(Cmat, x, self.lam1, self.lam2, self.inds, self.grpNUM, self.mu)