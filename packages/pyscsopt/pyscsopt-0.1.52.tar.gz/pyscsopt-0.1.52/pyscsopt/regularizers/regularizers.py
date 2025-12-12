import jax.numpy as jnp

def indbox_f(x, lb, ub):
    if jnp.any(x < lb) or jnp.any(x > ub):
        return jnp.inf
    else:
        return 0.0

def get_reg(model, x, reg_name):
    if reg_name == "l1":
        return model.lam * jnp.sum(jnp.abs(x))
    elif reg_name == "l2":
        return model.lam * jnp.sum(x ** 2)
    elif reg_name == "indbox":
        lb, ub = model.C_set[0], model.C_set[1]
        return indbox_f(x, lb, ub)
    elif reg_name == "gl":
        if len(model.lam) != 2:
            raise ValueError("Please provide a tuple or list with exactly two entries for lam, e.g. [lam1, lam2]")
        P = model.P
        Px = P.matrix @ x
        lam1, lam2 = model.lam[0], model.lam[1]
        return lam2 * P.Lasso_fz(Px) + lam1 * jnp.sum(jnp.abs(x))
    else:
        raise ValueError("reg_name not valid.")