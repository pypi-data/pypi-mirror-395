"""Functions to validate input for NMFProfiler."""

# Authors: Aurelie Mercadie
#          Eleonore Gravier
#          Gwendal Josse
#          Nathalie Vialaneix https://nathalievialaneix.eu
#          Celine Brouard https://miat.inrae.fr/brouard/
# License: GPL-3

import numpy as np
import warnings


def _check_type(input, type):
    return isinstance(input, type)


def _check_modalities(input, modalities):
    return input in modalities


def _check_inputs_NMFProfiler(X):
    """Check inputs of NMFProfiler (i.e. omic1, omic2, and so on).
    """
    params_names = [
        "alpha",
        "eta",
        "gamma",
        "lambda",
        "m_back",
        "mu",
        "sigma"
    ]
    init_methods = [
        'random',
        'random2',
        'random3',
        'nndsvd',
        'nndsvd2',
        'nndsvd3',
        'nndsvda',
        'nndsvdar'
    ]

    for j in range(len(X.omics)):
        if _check_type(X.omics[j], np.ndarray) is False:
            raise TypeError(
                f"Received {type(X.omics[j])}, "
                f"item number {j+1} in 'omics' (i.e. omic{j+1}) "
                "should be a numpy.ndarray."
            )
        if X.omics[0].shape[0] != X.omics[j].shape[0]:  # check dimensions
            raise Exception(
                "All datasets should have the exact same samples, but "
                f"omic1 (item 1 in 'omics') has {X.omics[0].shape[0]} samples "
                f"and omic{j+1} (item {j+1} in 'omics') has "
                f"{X.omics[j].shape[0]} samples. Please check datasets."
            )

    if _check_type(X.y, np.ndarray) is False:
        raise TypeError(
            f"Received {type(X.y)}, "
            "'y' should be a 1D numpy.ndarray."
        )
    if X.y.shape[0] != X.omics[0].shape[0]:  # check dimensions
        raise Exception(
            f"Group vector y has {X.y.shape[0]} samples but "
            f"omic1 (item 1 in 'omics') has {X.omics[0].shape[0]} samples. "
            "Please check datasets."
        )
    if len(np.unique(X.y)) < 2:  # check y values
        raise Exception(
            "At least two different levels needed in group vector y."
        )

    if _check_type(X.params, dict) is False:
        raise TypeError(
            f"Received {type(X.params)}, "
            "'params' parameter should be a dictionary."
        )
    if all(param in X.params for param in params_names) is False:
        raise ValueError(
            "One or more essential key-value pair(s) missing. "
            "See documentation."
        )
    if len(X.params) > 7:
        raise ValueError(
            "Extra key-value pair(s), 'params' should be of length 7. "
            "See documentation."
        )
    if _check_type(X.params['alpha'], int) is False or X.params['alpha'] < 1:
        raise TypeError(
            f"Received {X.params['alpha']} {type(X.params['alpha'])}, "
            "'alpha' should be a positive integer."
        )
    if _check_type(X.params['eta'], float) is False or X.params['eta'] <= 0:
        raise TypeError(
            f"Received {X.params['eta']} {type(X.params['eta'])}, "
            "'eta' should be a positive float."
        )
    if _check_type(X.params['gamma'], float) is False or X.params['gamma'] < 0:
        raise TypeError(
            f"Received {X.params['gamma']} {type(X.params['gamma'])}, "
            "'gamma' should be a non-negative float."
        )
    if (_check_type(X.params['lambda'], float) is False or
            X.params['lambda'] < 0):
        raise TypeError(
            f"Received {X.params['lambda']} {type(X.params['lambda'])}, "
            "'lambda' should be a non-negative float."
        )
    if _check_type(X.params['m_back'], int) is False or X.params['m_back'] < 1:
        raise TypeError(
            f"Received {X.params['m_back']} {type(X.params['m_back'])}, "
            "'m_back' should be a positive integer."
        )
    if _check_type(X.params['mu'], float) is False or X.params['mu'] < 0:
        raise TypeError(
            f"Received {X.params['mu']} {type(X.params['mu'])}, "
            "'mu' should be a non-negative float."
        )
    if (_check_type(X.params['sigma'], float) is False or
            X.params['sigma'] <= 0):
        raise TypeError(
            f"Received {X.params['sigma']} {type(X.params['sigma'])}, "
            "'sigma' should be a positive float."
        )

    if _check_modalities(X.init_method, init_methods) is False:
        raise ValueError(
            f"Received '{X.init_method}', which is not a valid choice "
            "for 'init_method'. Please, check documentation and change "
            " accordingly."
        )

    if _check_modalities(X.solver, ['analytical', 'autograd']) is False:
        raise ValueError(
            f"Received '{X.solver}'. Choices for 'solver' parameter "
            "are 'analytical' and 'autograd'. Please, change this "
            "parameter accordingly."
        )

    if _check_type(X.as_sklearn, bool) is False:
        raise TypeError(
            f"Received {type(X.as_sklearn)}, "
            "'as_sklearn' parameter should be a boolean."
        )

    if _check_type(X.backtrack, bool) is False:
        raise TypeError(
            f"Received {type(X.backtrack)}, "
            "'backtrack' parameter should be a boolean."
        )
    if X.as_sklearn is False:
        if X.backtrack is False:
            warnings.warn(
                "Proximal updates should be used with the backtracking "
                "linesearch procedure, otherwise results quality "
                "might be strongly impacted."
            )

    if _check_type(X.max_iter, int) is False or X.max_iter < 1:
        raise TypeError(
            f"Received {X.max_iter} ({type(X.max_iter)}), "
            "'max_iter' parameter should be a positive integer."
        )

    if _check_type(X.max_iter_back, int) is False or X.max_iter_back < 1:
        raise TypeError(
            f"Received {X.max_iter_back} ({type(X.max_iter_back)}), "
            "'max_iter_back' parameter should be a positive integer."
        )

    if _check_type(X.tol, float) is False or X.tol < 0:
        raise TypeError(
            f"Received {X.tol} ({type(X.tol)}), "
            "'tol' parameter should be a non-negative float."
        )

    if _check_type(X.seed, int) is False and X.seed is not None:
        raise TypeError(
            f"Received {type(X.seed)}, "
            "'seed' parameter should be an integer or 'None'."
        )

    if _check_type(X.verbose, bool) is False:
        raise TypeError(
            f"Received {type(X.verbose)}, "
            "'verbose' parameter should be a boolean."
        )
