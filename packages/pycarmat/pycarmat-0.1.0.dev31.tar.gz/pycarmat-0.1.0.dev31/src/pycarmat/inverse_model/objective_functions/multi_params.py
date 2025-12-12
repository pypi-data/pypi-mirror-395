from copy import deepcopy

from numpy import ones_like, abs, asarray

from qosm.propagation import GBTC


def cost_function(x, freq_ghz, metric_fn, kwargs):
    s21_meas = kwargs['s21_meas']
    use_abs = kwargs.get('use_abs', True)

    model = kwargs.get('model', GBTC)
    config = kwargs.get('config')
    unknown_layer = kwargs.get('unknown_layer')
    theta_y_deg_array = kwargs.get('theta_y_deg_array')
    use_weights = kwargs.get('use_angular_weights', True)
    if use_weights:
        _w = kwargs.get('theta_weight_array', ones_like(theta_y_deg_array))
    else:
        _w = ones_like(theta_y_deg_array)
    unknown_thicknesses = kwargs.get('unknown_thicknesses', [])
    _config = deepcopy(config)
    _config['mut'][unknown_layer]['epsilon_r'] = x[0] + x[1] * 1j
    for _index, unknown_thickness in enumerate(unknown_thicknesses):
        _config['mut'][unknown_thickness]['thickness'] = x[_index+2] * 1e-3

    _arr_sim = []
    _arr_meas = []

    for ii, theta_deg in enumerate(theta_y_deg_array):
        _config['sample_attitude_deg'] = (0, theta_deg, 0)
        _s11, _, _s21, _ = model.simulate(_config, freq_ghz)
        _arr_sim.append(_s21.real * _w[ii])
        _arr_sim.append(_s21.imag * _w[ii])
        _arr_meas.append(s21_meas[ii].real * _w[ii])
        _arr_meas.append(s21_meas[ii].imag * _w[ii])
        if use_abs:
            _arr_sim.append(abs(_s21) * _w[ii])
            _arr_meas.append(abs(s21_meas[ii]) * _w[ii])

    return metric_fn(asarray(_arr_meas), asarray(_arr_sim))
