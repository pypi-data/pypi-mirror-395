import numpy as np
from datetime import datetime

class Solution:
    def __init__(self, x, obj, fval, fvaltest, rel, objrel, metricvals, times, epochs, model, pri_res_norms=None):
        self.x = x
        self.obj = obj
        self.fval = fval
        self.fvaltest = fvaltest
        self.rel = rel
        self.objrel = objrel
        self.metricvals = metricvals
        self.times = times
        self.epochs = epochs
        self.model = model
        self.pri_res_norms = pri_res_norms

class Options:
    def __init__(self, metrics=None, alpha=None, batch_size=None, slice_samples=False, shuffle_batch=True, max_epoch=1, max_iter=None, comm_rounds=100, local_max_iter=None, x_tol=1e-10, f_tol=1e-10, verbose=1, patience=3):
        self.metrics = metrics
        self.alpha = alpha
        self.batch_size = batch_size
        self.slice_samples = slice_samples
        self.shuffle_batch = shuffle_batch
        self.max_epoch = max_epoch
        self.max_iter = max_iter
        self.comm_rounds = comm_rounds
        self.local_max_iter = local_max_iter
        self.x_tol = x_tol
        self.f_tol = f_tol
        self.verbose = verbose
        self.patience = patience

def iter_step(method, model, reg_name, hmu, As, x, x_prev, ys, Cmat, iter):
    return method.step(model, reg_name, hmu, As, x, x_prev, ys, Cmat, iter)

def iterate(method, model, reg_name, hmu, metrics=None, alpha=None, batch_size=None, slice_samples=False, shuffle_batch=True, max_epoch=1000, comm_rounds=100, local_max_iter=None, x_tol=1e-10, f_tol=1e-10, verbose=1, patience=None):
    opt = Options(
        metrics=metrics,
        batch_size=batch_size,
        slice_samples=slice_samples,
        shuffle_batch=shuffle_batch,
        max_epoch=1 if local_max_iter is not None else max_epoch,
        comm_rounds=comm_rounds,
        local_max_iter=local_max_iter,
        x_tol=x_tol,
        f_tol=f_tol,
        verbose=verbose,
        patience=patience if patience is not None else max_epoch+1
    )
    if alpha is not None:
        model.L = 1.0/alpha
    return optim_loop(method, model, reg_name, hmu, opt)

def optim_loop(method, model, reg_name, hmu, opt):
    is_generic = (model.A is None or model.y is None)
    x = model.x0.copy()
    x_prev = x.copy()
    epochs = 0
    objs, fvals, rel_errors, objrels, times = [], [], [], [], []
    pri_res_norms = []
    t0 = datetime.now()
    # Print optimization header
    if opt.verbose > 0:
        print("\n========== Optimization Started ==========")
        print(f"Method:      {getattr(method, 'name', str(method))}")
        print(f"Model:       {getattr(model, 'name', type(model).__name__)}")
        print(f"Regularizer: {reg_name}")
        print(f"Max Epochs:  {opt.max_epoch}")
        print(f"x_tol:       {opt.x_tol:.1e} | f_tol: {opt.f_tol:.1e} | Patience: {opt.patience}")
        print(f"Start Time:  {t0.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*50)
        header_fmt = "{:<5s} | {:>12s} | {:>12s} | {:>10s} | {:>10s} | {:>12s}"
        row_fmt =    "{:<5d} | {:>12.4e} | {:>12.4e} | {:>10.4e} | {:>10.2e} | {:>12.2e}"
        print(header_fmt.format('Epoch', 'obj', 'fval', 'rel_err', 'objrel', 'pri_res_norm'))
        print("-"*77)
    # initialize the method with the starting point x (important for BFGS/Hessian-based methods)
    if method is not None and hasattr(method, 'init'):
        method.init(x)
    if is_generic:
        f = lambda x: model.f(x)
    else:
        f = lambda x: model.f(model.A, model.y, x)
    n = x.shape[0]
    patience_counter = 0
    best_fval = None
    converged_reason = None
    for epoch in range(opt.max_epoch):
        fval = f(x)
        obj = fval + model.get_reg(x, reg_name)
        fvals.append(fval)
        objs.append(obj)
        rel_error = np.linalg.norm(x - x_prev)/max(np.linalg.norm(x_prev), 1)
        rel_errors.append(rel_error)
        objrel = abs(obj - (f(x_prev) + model.get_reg(x_prev, reg_name)))/max(abs((f(x_prev) + model.get_reg(x_prev, reg_name))), 1)
        objrels.append(objrel)
        times.append((datetime.now() - t0).total_seconds())
        if reg_name == "gl" and hasattr(model, "P") and hasattr(model.P, "Cmat"):
            Cmat = model.P.Cmat
        else:
            Cmat = np.eye(n)
        if best_fval is None or fval < best_fval:
            best_fval = fval
            patience_counter = 0
        else:
            patience_counter += 1
        if patience_counter >= opt.patience:
            converged_reason = f"Patience level {opt.patience} reached at epoch {epoch+1}, stopping early."
            if opt.verbose > 0:
                print(f"Patience level {opt.patience} reached at epoch {epoch+1}, stopping early.")
            break
        if patience_counter < opt.patience - 1:
            if is_generic:
                x_new, pri_res_norm = iter_step(method, model, reg_name, hmu, None, x, x_prev, None, Cmat, epoch)
            else:
                x_new, pri_res_norm = iter_step(method, model, reg_name, hmu, model.A, x, x_prev, model.y, Cmat, epoch)
            pri_res_norms.append(pri_res_norm)
            if opt.verbose > 0:
                # Only print titles if not about to break
                will_break = (
                    np.linalg.norm(x_new - x) < opt.x_tol*max(np.linalg.norm(x), 1)
                    or pri_res_norm < opt.x_tol * max(1, np.linalg.norm(x))
                )
                if (epoch+1) % 7 == 1 and epoch != 0 and not will_break:
                    print("-"*77)
                    print(header_fmt.format('Epoch', 'obj', 'fval', 'rel_err', 'objrel', 'pri_res_norm'))
                    print("-"*77)
                print(row_fmt.format(epoch+1, obj, fval, rel_error, objrel, pri_res_norm))
            if (
                np.linalg.norm(x_new - x) < opt.x_tol*max(np.linalg.norm(x), 1)
                or pri_res_norm < opt.x_tol * max(1, np.linalg.norm(x))
                ):
                if np.linalg.norm(x_new - x) < opt.x_tol*max(np.linalg.norm(x), 1):
                    converged_reason = f"Converged: ||x_new - x|| < x_tol at epoch {epoch+1}."
                elif pri_res_norm < opt.x_tol * max(1, np.linalg.norm(x)):
                    converged_reason = f"Converged: pri_res_norm < x_tol at epoch {epoch+1}."
                break
            x_prev = x.copy()
            x = x_new.copy()
            epochs += 1
        else:
            # pri_res_norms.append(np.nan)
            converged_reason = f"Stopped at epoch {epoch+1} due to patience policy."
            break
    t1 = datetime.now()
    if opt.verbose > 0:
        print("-"*77)
        print(f"Optimization finished at {t1.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total epochs: {epochs}")
        print(f"Elapsed time: {(t1-t0).total_seconds():.2f} seconds")
        print(f"Best fval:    {np.min(fvals):.6e}")
        print(f"Best obj:     {np.min(objs):.6e}")
        print(f"Final rel_error: {rel_errors[-1]:.2e}")
        print(f"Final objrel:   {objrels[-1]:.2e}")
        if converged_reason:
            print(f"Convergence reason: {converged_reason}")
        print("========== Optimization Complete =========\n")
    return Solution(x, objs, fvals, None, rel_errors, objrels, pri_res_norms, times, epochs, model, pri_res_norms=pri_res_norms)