import numpy as np

# Proximal operator implementations

def prox_l1(x, h_scale, lam, alpha):
    t = alpha * lam / h_scale
    return np.sign(x) * np.maximum(np.abs(x) - t, 0)

def prox_l2(x, h_scale, lam, alpha):
    t = alpha * lam / h_scale
    denom = np.abs(x)
    denom[denom == 0] = 1e-12
    return x * np.maximum(1 - t/denom, 0)

def prox_indbox(x, model, h_scale, lam, alpha):
    lb, ub = model.C_set[0], model.C_set[1]
    return np.minimum(np.maximum(x, lb), ub)

def prox_grouplasso(x, model, h_scale, lam, alpha):
    P = model.P
    lam1, lam2 = model.lam[0], model.lam[1]
    t = lam1/h_scale
    utmp = np.sign(x) * np.maximum(np.abs(x) - t, 0)  # ProxL1
    u = P.ProxL2(utmp, alpha * lam2, h_scale)  # ProxL2 (assumed implemented in P)
    return u

def invoke_prox(model, reg_name, x, h, lam, alpha):
    if reg_name == "l1":
        return prox_l1(x, h, lam, alpha)
    elif reg_name == "l2":
        return prox_l2(x, h, lam, alpha)
    elif reg_name == "indbox":
        return prox_indbox(x, model, h, lam, alpha)
    elif reg_name == "gl":
        return prox_grouplasso(x, model, h, lam, alpha)
    else:
        raise ValueError("reg_name not valid.")