import numpy as np
import scipy.sparse as sp
import jax.numpy as jnp
import scipy.linalg

L_INF_CACHE = -1e32
U_INF_CACHE = 1e32

def bounds_sanity_check(n, lb, ub):
    # Accept scalar or array for lb/ub, and broadcast as needed
    if isinstance(lb, (int, float)):
        lb = np.full(n, lb)
    if isinstance(ub, (int, float)):
        ub = np.full(n, ub)
    lb = np.asarray(lb)
    ub = np.asarray(ub)
    na = lb.size
    nb = ub.size
    if na == n and nb == n:
        a = lb
        b = ub
    else:
        raise ValueError("Lengths of the bounds do not match that of the variable.")
    a = np.where(a == -np.inf, L_INF_CACHE, a)
    b = np.where(b == np.inf, U_INF_CACHE, b)
    return a, b

def twonorm(z, g_start, g_end):
    return jnp.linalg.norm(z[g_start:g_end+1])

def fz(z, ind, grpNUM):
    fz_val = 0.0
    for j in range(grpNUM):
        g_start = int(ind[0, j])
        g_end = int(ind[1, j])
        nrmval = twonorm(z, g_start, g_end)
        fz_val += ind[2, j] * nrmval
    return fz_val

def ProjL2(x, lam, h, inds, grpNUM):
    Px = np.zeros_like(x)
    ind = inds.flatten(order='F')
    for j in range(grpNUM):
        beta_g = lam * ind[2+3*j]
        g_start = int(ind[3*j])
        g_end = int(ind[1+3*j])
        nrmval = twonorm(x / h, g_start, g_end)
        for k in range(g_start, g_end+1):
            Px[k] = x[k] * min(beta_g / (h[k] * nrmval), 1)
    return Px

def ProxL2(x, lam, h, inds, grpNUM):
    Px = np.zeros_like(x)
    ind = inds.flatten(order='F')
    for j in range(grpNUM):
        beta_g = lam * ind[2+3*j]
        g_start = int(ind[3*j])
        g_end = int(ind[1+3*j])
        nrmval = twonorm(x, g_start, g_end)
        for k in range(g_start, g_end+1):
            Px[k] = x[k] * max(1 - beta_g / (h[k] * nrmval), 0)
    return Px

def get_Cmat(ind, grpSIZES, n):
    grpNUM = ind.shape[1]
    g_start = ind[0, :]
    g_end = ind[1, :]
    T = np.zeros((grpNUM, n), dtype=bool)
    for g in range(grpNUM):
        T[g, g_start[g]:g_end[g]+1] = 1
    Tw = ind[2, :]
    V, K = T.shape
    SV = np.sum(grpSIZES)
    J = np.zeros(SV, dtype=int)
    W = np.zeros(SV)
    idx = 0
    for v in range(V):
        idxs = np.where(T[v, :])[0]
        J[idx:idx+len(idxs)] = idxs
        W[idx:idx+len(idxs)] = Tw[v]
        idx += len(idxs)
    C = sp.coo_matrix((W, (np.arange(SV), J)), shape=(SV, K)).tocsc()
    return C

class get_P:
    def __init__(self, grpNUM, grpSIZES, ntotal, ind, G, matrix, Cmat, Pi, tau, times, trans, ProjL2, ProxL2, Lasso_fz):
        self.grpNUM = grpNUM
        self.grpSIZES = grpSIZES
        self.ntotal = ntotal
        self.ind = ind
        self.G = G
        self.matrix = matrix
        self.Cmat = Cmat
        self.Pi = Pi
        self.tau = tau
        self.times = times
        self.trans = trans
        self.ProjL2 = ProjL2
        self.ProxL2 = ProxL2
        self.Lasso_fz = Lasso_fz

def get_P_func(n, G, ind):
    grpNUM = ind.shape[1]
    grpSIZES = (ind[1, :] - ind[0, :] + 1)
    ntotal = np.sum(grpSIZES)
    row = np.arange(ntotal)
    col = G
    data = np.ones(ntotal)
    Pmat = sp.coo_matrix((data, (row, col)), shape=(ntotal, n)).tocsc()
    Pmat_dense = Pmat.toarray() if hasattr(Pmat, 'toarray') else np.array(Pmat)
    Pmat_jax = jnp.array(Pmat_dense)
    def P_i(i):
        tmp = grpSIZES[i]
        I = np.arange(tmp)
        J = G[ind[0, i]:ind[1, i]+1]
        V = np.ones(tmp)
        Pi = sp.coo_matrix((V, (I, J)), shape=(tmp, n)).tocsc()
        Pi_dense = Pi.toarray() if hasattr(Pi, 'toarray') else np.array(Pi)
        return jnp.array(Pi_dense)
    Cmat = get_Cmat(ind, grpSIZES, n)
    Cmat_dense = Cmat.toarray() if hasattr(Cmat, 'toarray') else np.array(Cmat)
    Cmat_jax = jnp.array(Cmat_dense)
    return get_P(
        grpNUM,
        grpSIZES,
        ntotal,
        ind,
        G,
        Pmat_jax,
        Cmat_jax,
        P_i,
        1.0,
        lambda x: Pmat_jax @ x,
        lambda y: Pmat_jax.T @ y,
        lambda z, c1, h: ProjL2(z, c1, h, ind, grpNUM),
        lambda z, c1, h: ProxL2(z, c1, h, ind, grpNUM),
        lambda z: fz(z, ind, grpNUM)
    )

def make_group_lasso_problem(m, n, grpsize=5, p_active=0.1, noise_std=0.1, seed=None, group_weights=1.0, use_const_grpsize=True, corr=0.5):
    """
    Utility to generate a synthetic group lasso regression problem.
    According to the paper "GAP Safe Screening Rules for Sparse-Group Lasso". See https://github.com/EugeneNdiaye/GAPSAFE_SGL
    Args:
        m: number of samples
        n: number of features
        grpsize: size of each group (int or list of ints)
        p_active: proportion of groups that are active (float in (0,1])
        noise_std: standard deviation of noise
        seed: random seed
        group_weights: scalar or list of group weights
        use_const_grpsize: if True, all groups have size grpsize
        corr: correlation for Toeplitz covariance
    Returns:
        A, y, x_true, x0, groups, ind, P
    """
    rng = np.random.default_rng(seed)
    # Group structure
    if use_const_grpsize:
        n_groups = n//grpsize
        groups = [range(i*grpsize, min((i+1)*grpsize, n)) for i in range(n_groups)]
    else:
        splits = np.sort(rng.choice(np.arange(1, n), size=n//grpsize-1, replace=False))
        groups = np.split(np.arange(n), splits)
        n_groups = len(groups)
    # Group weights
    if np.isscalar(group_weights):
        group_weights = [group_weights] * n_groups
    # True coefficients: only a proportion p_active of groups are nonzero
    x_true = np.zeros(n)
    n_active_groups = max(1, int(np.ceil(n_groups * p_active)))
    active_groups = rng.choice(n_groups, size=n_active_groups, replace=False)
    for g in active_groups:
        g_idx = groups[g]
        # For each active group, only a proportion p_active of features are nonzero
        n_features = len(g_idx)
        n_active_features = max(1, int(np.ceil(n_features * p_active)))
        selected_features = rng.choice(g_idx, size=n_active_features, replace=False)
        s = 2 * rng.random(n_active_features) - 1
        u = rng.random(n_active_features)
        x_true[selected_features] = np.sign(s) * (10 * u + (1 - u) * 0.5)
    # Toeplitz covariance for correlated features
    cov = scipy.linalg.toeplitz(corr ** np.arange(n))
    A = rng.multivariate_normal(np.zeros(n), cov, size=m)
    y = A @ x_true + noise_std * rng.normal(size=m)
    x0 = np.zeros(n)
    # ind matrix for group lasso
    ind = np.zeros((3, n_groups), dtype=int)
    for j, g in enumerate(groups):
        ind[0, j] = g.start if isinstance(g, range) else g[0]
        ind[1, j] = g.stop - 1 if isinstance(g, range) else g[-1]
        ind[2, j] = group_weights[j]
    G = np.arange(n)
    P = get_P_func(n, G, ind)
    return A, y, x_true, x0, groups, ind, P
