import numpy as np

def mean_square_error(xtrue, xpred):
    return np.mean((xtrue - xpred) ** 2)

def linesearch(x, d, f, grad_f, max_iter=50, tol=1e-6):
    alpha = 1.0
    rho = 0.5
    c = 1e-4
    for _ in range(max_iter):
        if f(x + alpha * d) <= f(x) + c * alpha * np.dot(grad_f(x), d):
            break
        if np.abs(alpha) < tol:
            break
        alpha *= rho
    return alpha

# compute inverse of the Barzilai-Borwein step size to estimate alpha in the paper
## see https://en.wikipedia.org/wiki/Barzilai-Borwein_method
def inv_BB_step(x, x_prev, gradx, gradx_prev):
    delta = x - x_prev
    gamma = gradx - gradx_prev
    denom = np.dot(delta, gamma)
    if denom == 0:
        return 1.0
    L_est = np.dot(gamma, gamma) / denom
    return L_est