from numpy import ones_like, sum, abs, linalg, real, imag, full_like, tanh
from sklearn.metrics import r2_score as r2


def lsq_score(ref, sim, weight=None):
    if weight is None:
        weight = ones_like(ref)
    res = ref - sim
    cost = sum(abs(weight * res) ** 2)
    return cost


def l2_score(ref, sim, weight=None):
    if weight is None:
        weight = ones_like(ref)
        weight /= linalg.norm(weight)
    error = linalg.norm(weight * (ref - sim), ord=2)
    error /= linalg.norm(weight * (ref + sim), ord=2)
    return error

def r2_score(ref, sim, is_complex: bool = True):
    r2_re = r2(real(ref), real(sim))
    r2_re_bounded = max(-1, min(1, r2_re))
    if is_complex:
        r2_im = r2(imag(ref), imag(sim))
        r2_im_bounded = max(-1, min(1, r2_im))
        return .5 * ((1 - r2_re_bounded) / 2 + (1 - r2_im_bounded) / 2)
    else:
        return (1 - r2_re_bounded) / 2

def tanh_score_nd(ref, sim, weight=None, alpha=.1):
    if weight is None:
        weight = ones_like(ref)
        weight /= linalg.norm(weight)
    try:
        err1 = full_like(sim, 0)
        err2 = full_like(sim, 0)
        idx1 = abs(sim) != 0
        idx2 = abs(ref) != 0
        err1[idx1] = 1 - ref[idx1] / sim[idx1]
        err2[idx2] = 1 - sim[idx2] / ref[idx2]
    except TypeError:
        err1 = 1 - ref / sim if abs(sim) > 0 else 0
        err2 = 1 - sim / ref if abs(ref) > 0 else 0
    except IndexError:
        err1 = 1 - ref / sim if abs(sim) > 0 else 0
        err2 = 1 - sim / ref if abs(ref) > 0 else 0
    error = linalg.norm(weight * tanh(alpha * abs(err1 * err2)))
    return error

def tanh_score_1d(ref, sim, alpha=.1):
    err1 = 1 - ref / sim if abs(sim) > 0 else 0
    err2 = 1 - sim / ref if abs(ref) > 0 else 0
    return tanh(alpha * abs(err1 * err2))

def tanh_score_1d2(ref, sim, alpha=.1):
    err = 1 - sim / ref if abs(ref) > 0 else 0
    return tanh(alpha * abs(err)**2)