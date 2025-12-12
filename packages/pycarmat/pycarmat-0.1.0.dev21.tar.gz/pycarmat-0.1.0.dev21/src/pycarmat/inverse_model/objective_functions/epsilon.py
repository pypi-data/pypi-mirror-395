import inspect
from copy import deepcopy

from numpy import ones_like, abs, asarray
from qosm.propagation import PW


def cost_function(x, freq_ghz, metric_fn, kwargs):
    config = kwargs['config']
    s21_meas = kwargs['s21_meas']
    phys_constraint = kwargs.get('phys_constraint', True)
    coefficient_3d = kwargs.get('coefficient_3d', 10)
    unknown_layer = kwargs.get('unknown_layer')
    model = kwargs.get('model', PW)

    config['mut'][unknown_layer]['epsilon_r'] = x[0] + 1j * x[1]
    _, s12_model, s21_model, _ = model.simulate(config, freq_ghz)

    penalty = (1e10 if x[1] > 0 else 0) if phys_constraint else 0

    sig = inspect.signature(metric_fn)
    if 'alpha' in sig.parameters:
        res = abs(metric_fn(s21_meas, .5*(s21_model + s12_model), alpha=1 / coefficient_3d) + penalty)
    else:
        res = abs(metric_fn(s21_meas, .5*(s21_model + s12_model)) + penalty)
    return res