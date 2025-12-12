"""NMFProfiler: A multi-omics integration method for samples stratified in
groups
"""

# Authors: Aurelie Mercadie
#          Eleonore Gravier
#          Gwendal Josse
#          Nathalie Vialaneix https://nathalievialaneix.eu
#          Celine Brouard https://miat.inrae.fr/brouard/
# License: GPL-3

from copy import deepcopy

import itertools

import warnings
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
from numpy import divide, multiply, newaxis
from numpy.linalg import norm, multi_dot
import pandas as pd

from sklearn.decomposition._nmf import _initialize_nmf
from sklearn.utils.extmath import safe_sparse_dot
from sklearn.preprocessing import OneHotEncoder
from sklearn.exceptions import ConvergenceWarning

import statsmodels.api as sm

from time import process_time  # closest to elapsed time from system.time() (R)

from .utils.validate_inputs import _check_inputs_NMFProfiler


def _prox_l1_pos(v, lambd):
    """Proximal operator of l1 norm (lasso) + positivity constraint."""
    return np.maximum(v - lambd, 0)


def _update_W(W, omics, Hs, mu):
    """Update the matrix containing contributions of individuals to latent
    components.

    Parameters
    ----------
    :W: ndarray of shape (n_samples x K), contributions of individuals
        to latent components.
    :omics: list of (n_omics) ndarrays of shape (n_samples x n_features_omicj),
        values of features from (omicj) measured on the same
        (n_samples) samples.
    :Hs: list of (n_omics) ndarrays of shape (K x n_features_omicj),
        latent components built on (omicj).
    :mu: float, value for parameter `mu` from objective function.


    Returns
    -------
    Newly updated W.
    """
    B = mu * np.identity(W.shape[1])
    for j in range(len(Hs)):
        B += safe_sparse_dot(Hs[j], Hs[j].T)
    C = np.zeros((W.shape[0], W.shape[1]))
    for j in range(len(Hs)):
        C += safe_sparse_dot(omics[j], Hs[j].T)

    return multiply(W, divide(C, safe_sparse_dot(W, B)))


def _update_H(
    H,
    W,
    omic,
    Beta,
    Y,
    gamma,
    eta,
    lambdA,
    as_sklearn,
    grad=False,
    H_grad=None
):
    """Update the matrix containing latent components built on omic j.
       (j referring to the omic dataset number, between 1 and J)

    Parameters
    ----------
    :H: ndarray of shape (K x n_features_omicj), latent components built on
        omic j.
    :W: ndarray of shape (n_samples x K), contributions of individuals to
        latent components.
    :omic: ndarray of shape (n_samples x n_features_omicj), values of
        features from omic j measured on (n_samples).
    :Beta: ndarray of shape (K x 1), regression coefficients for projection
        of individuals from omic j onto latent components from H^(j).
    :Y: ndarray of shape (n_samples x U), one-hot encoding of (y) indicating
        to which group each sample belongs.
    :gamma: float, nonnegative value for parameter `gamma` from objective
        function.
    :eta: float, nonnegative value for parameter `eta` from prox.
    :lambdA: float, nonnegative value for parameter `lambda` from objective
        function.
    :as_sklearn: boolean, whether or not a modified version of the MU updates
        from scikit-learn is used.
    :grad: boolean, compute gradient or not. By default, grad = False.
    :H_grad: list, gradient values of H^(j) matrix. By default, H_grad = None.


    Returns
    -------
    Newly updated H^(j).


    Note
    ----
    A part of this function is strongly based on Multiplicative Updates
    implemented in sklearn.decomposition.NMF.
    """
    R = safe_sparse_dot(W.T, omic) + (
        gamma * multi_dot([np.diag(Beta), Y.T, omic])
    )  # R (Prox) or numerator (MU)
    D = multi_dot([W.T, W, H]) + (
        gamma * multi_dot([np.diag(Beta**2), H, omic.T, omic])
    )  # D (Prox) or denominator (MU)

    # Compute gradient before updates
    if grad:
        H_grad.append(D - R)

    if as_sklearn:
        EPSILON = np.finfo(np.float32).eps

        # Add L1 regularization
        if lambdA > 0:
            D += lambdA

        # Introduce small value to avoid definition problems
        D[D == 0] = EPSILON

        delta_H = R
        delta_H /= D
        H *= delta_H

    else:
        H_tilde = H + (1 / eta) * (R - D)
        H = _prox_l1_pos(H_tilde, lambdA / eta)

    return [H, H_grad] if grad else H


def _update_Beta(omic, h_k, y_k, gamma, Beta):
    """Update the regression coefficients linked to omic j and component k.
    (j referring to the omic dataset number, between 1 and J)

    Parameters
    ----------
    :omic: ndarray of shape (n_samples x n_features_omicj), values of
        features from omic j measured on (n_samples).
    :h_k: ndarray of length (n_features_omicj), contains latent component k
        built on omic j (row k of H^(j)).
    :y_k: ndarray of length (n_samples), contains binary labels regarding
        group k (column k of Y).
    :gamma: float, value for parameter `gamma` from objective function.
    :Beta: float, regression coefficient for projection of individuals from
        omic j onto latent components from H^(j).


    Returns
    -------
    Newly updated scalar Beta_k^(j).
    """
    if gamma > 0:

        h_k = h_k[newaxis]  # 1 component x p_j features
        y_k = np.transpose(y_k[newaxis])  # n samples x 1 group

        u_numerator = np.squeeze(
            multi_dot([h_k, omic.T, y_k])
        )  # np.squeeze to reduce to a 0d array
        u_denominator = np.squeeze(
            multi_dot([h_k, omic.T, omic, np.transpose(h_k)])
        )  # np.squeeze to reduce to a 0d array

        Beta = divide(u_numerator, u_denominator)

    return Beta


def _computeF(
    omics,
    Y,
    W,
    Hs,
    Betas,
    mu,
    lambdA,
    gamma,
    K_gp,
    details=False
):
    """Compute the value of F given Y, W, each omicj, Hj, Betaj
    and some hyperparameters (i.e. gamma, lambda and mu).

    Calculate the objective function value, as well as each error term,
    in order to monitor progress of algorithm convergence.

    Parameters
    ----------
    :omics: list of (n_omics) ndarrays of shape (n_samples x n_features_omicj),
        values of features from (omicj) measured on the same
        (n_samples) samples.
    :Y: ndarray of shape (n_samples x U), one-hot encoding of (y) indicating
        to which group each sample belongs.
    :W: ndarray of shape (n_samples x K), contributions of individuals to
        latent components.
    :Hs: list of (n_omics) ndarrays of shape (K x n_features_omicj),
        latent components built on (omicj).
    :Betas: list of (n_omics) ndarrays of shape (K x 1), regression
        coefficients for projection of individuals from (omicj)
        onto latent components from H^(j).
    :mu: float, value for parameter `mu` from objective function.
    :lambdA: float, value for parameter `lambda` from objective function.
    :gamma: float, value for parameter `gamma` from objective function.
    :K_gp: int, number of components dedicated to groups profiling.
    :details: boolean, whether or not all specific error terms are displayed
        to the user. By default, details = False.


    Returns
    -------
    Either the value of the objective function (i.e. the global loss) alone,
    or accompagned by each specific term to obtain it.
    """
    regul = (mu / 2) * np.trace(safe_sparse_dot(W.T, W))
    distort, sparse, pred = ([] for i in range(3))
    for j in range(len(omics)):
        distort.append(0.5 * (norm(omics[j] - safe_sparse_dot(W, Hs[j])) ** 2))
        sparse.append(lambdA * norm(Hs[j], 1))
        pred.append(
            (gamma / 2) * (
                norm(Y - multi_dot([omics[j], Hs[j].T[:, 0:K_gp],
                                    np.diag(Betas[j][0:K_gp])])) ** 2
            )
        )

    loss = sum(distort) + regul + sum(sparse) + sum(pred)

    if details:
        res = [loss, distort, sparse, regul, pred]

    return loss if details is False else res


def _computeMargH(omic, Y, W, H, Beta, gamma, lambdA, K_gp):
    """Compute the marginal loss of H^(j).

    Calculate the marginal of the objective function in H^(j) to perform
    Backtrack LineSearch and optimize the value of the gradient descent step
    size eta^(j).

    Parameters
    ----------
    :omic: ndarray of shape (n_samples x n_features_omicj), values of
        features from omic j measured on (n_samples).
    :Y: ndarray of shape (n_samples x U), one-hot encoding of (y) indicating
        to which group each sample belongs.
    :W: ndarray of shape (n_samples x K), contributions of individuals to
        latent components.
    :H: ndarray of shape (K x n_features_omicj), latent components built on
        omic j.
    :Beta: ndarray of shape (K x 1), regression coefficients for projection
        of individuals from omic j onto latent components from H^(j).
    :gamma: float, value for parameters `gamma` from objective function.
    :lambdA: float, value for parameter `lambda` from objective function.
    :K_gp: int, number of components dedicated to groups profiling.


    Returns
    -------
    Value of the marginal loss for H^(j).
    """
    part1 = 0.5 * np.trace(multi_dot([H.T, W.T, W, H]))
    part2 = np.trace(multi_dot([H.T, W.T, omic]))
    part3 = (gamma / 2) * np.trace(
        multi_dot(
            [np.diag(Beta[0:K_gp] ** 2), H[0:K_gp, :],
             omic.T, omic, H.T[:, 0:K_gp]]
        )
    )
    part4 = gamma * np.trace(
        multi_dot([np.diag(Beta[0:K_gp]), H[0:K_gp, :], omic.T, Y])
    )
    part5 = lambdA * norm(H, 1)

    res = part1 - part2 + part3 - part4 + part5

    return res


def _linesearch(
    H_old,
    H,
    W,
    omic,
    Beta,
    Y,
    gamma,
    lambdA,
    current_eta,
    H_loss,
    alpha,
    sigma,
    m_back,
    max_iter_back,
    K_gp,
    verbose,
):
    """Find the most suited value for eta^(j).

    Calculate the optimal gradient descent step size eta^(j) to update H^(j)
    (j = 1,...,J).
    Instead of reuse each time the initial eta_0^(j), use the last one found,
    eta_(t-1)^(j).

    Parameters
    ----------
    :H_old: ndarray of shape (K x n_features_omicj), latent components built
        on omic j at t-1 (or t).
    :H: ndarray of shape (K x n_features_omicj), latent components built
        on omic j at t (or t+1).
    :W: ndarray of shape (n_samples x K), contributions of individuals to
        latent components.
    :omic: ndarray of shape (n_samples x n_features_omicj), values of
        features from omic j measured on (n_samples).
    :Beta: ndarray of shape (K x 1), regression coefficients for projection
        of individuals from omic j onto latent components from H^(j).
    :Y: ndarray of shape (n_samples x U), one-hot encoding of (y) indicating
        to which group each sample belongs.
    :gamma: float, value for parameters `gamma` from objective function.
    :lambdA: float, value for parameter `lambda` from objective function.
    :current_eta: float, last optimal value for parameter `eta` from proximal.
    :H_loss: list, values of the marginal loss in H.
    :alpha: float, factor by which multiplying eta^(j).
    :sigma: float, parameter needed in thr_back computation.
    :m_back: int, marginal loss historic looked at when optimizing eta^(j).
    :max_iter_back: int, maximum number of iterations for the backtrack.
    :K_gp: int, number of components dedicated to groups profiling.
    :verbose: boolean, whether or not to print algorithm progress.


    Returns
    -------
    :H: ndarray of shape (K x n_features_omicj), newly updated H^(j).
    :H_loss: list, updated with last marginal loss for H^(j).
    :current_eta: float, optimal value for eta^(j) chosen during linesearch.
    """

    # Initialize iteration
    it = 0

    # Compute the threshold under which the update of eta will stop
    thr_back = np.max(
        [
            H_loss[-2 - k] - (sigma / 2 * current_eta * norm(H - H_old) ** 2)
            for k in range(min(m_back, len(H_loss) - 1))
        ]
    )

    # Backtrack LineSearch
    while H_loss[-1] > thr_back and it < max_iter_back:
        current_eta *= alpha
        H = _update_H(
            H_old,
            W,
            omic,
            Beta,
            Y,
            gamma,
            current_eta,
            lambdA,
            as_sklearn=False
        )
        H_loss[-1] = _computeMargH(omic, Y, W, H, Beta, gamma, lambdA, K_gp)
        thr_back = np.max(
            [
                H_loss[-2 - k] - (
                    sigma / 2 * current_eta * norm(H - H_old) ** 2
                )
                for k in range(min(m_back, len(H_loss) - 1))
            ]
        )
        it += 1

    if it == max_iter_back and verbose:
        print("Warning: backtrack failed")

    return H, H_loss, current_eta


def _analytic_solver(
    omics,
    Y,
    W,
    Hs,
    Betas,
    params,
    current_etas,
    as_sklearn,
    backtrack,
    max_iter_back,
    Hlosses,
    Hgrads,
    K,
    K_gp,
    verbose,
):
    """Solver for NMFProfiler.

    This solver is based on analytic forms of gradients computed by hand.
    It has been adapted from both solvers in sklearn.decomposition.NMF and
    the one proposed by Fernsel and Maass (2018).


    Parameters
    ----------
    :omics: list of (n_omics) ndarrays of shape (n_samples x n_features_omicj),
        values of features from (omicj) measured on the same
        (n_samples) samples.
    :Y: ndarray of shape (n_samples x U), one-hot encoding of (y) indicating
        to which group each sample belongs.
    :W: ndarray of shape (n_samples x K), contributions of individuals to
        latent components, initialized or at (t).
    :Hs: list of (n_omics) ndarrays of shape (K x n_features_omicj),
        latent components built on (omicj), initialized or at (t).
    :Betas: list of (n_omics) ndarrays of shape (K x 1), regression
        coefficients for projection of individuals from (omicj)
        onto H^(j),initialized or at (t).
    :params: dict of length 7 (optional), values for parameters `gamma`,
        `lambda`, `mu` from objective function, `eta` for prox, and
        `alpha`, `sigma`, `m_back` for linesearch().
        By default, gamma = 0.005, lambda = 1e-3, mu = 1e-3, eta = 1,
        alpha = 2, sigma = 1e-9 and m_back = 1.
    :current_etas: list of (n_omics) floats, value of parameter `etaj`.
    :as_sklearn: boolean, whether or not a modified version of the MU updates
        from scikit-learn is used.
    :backtrack: boolean, if Backtrack LineSearch is performed or not.
    :max_iter_back: int, maximum number of iterations for the backtrack.
    :Hlosses: list of (n_omics) lists, vsalues of the marginal loss for H^(j).
    :Hgrads: list of (n_omics) lists, values of gradient in H^(j)
        (before update).
    :K: int (optional), number of latent components to build.
        By default, K = 2.
    :K_gp: int, number of components dedicated to groups profiling.
    :verbose: boolean, whether or not to print algorithm progress.


    Returns
    -------
    :W_new: ndarray of shape (n_samples x K), updated, or (t+1), W matrix.
    :Hs_new: list of (n_omics) ndarrays of shape (K x n_features_omicj),
        updated, or (t+1), Hj matrices.
    :Betas_new: list of (n_omics) vectors of length (K), updated, or (t+1),
        Betaj vectors.
    :current_etas: list of (n_omics) floats, updated value of parameter `etaj`.
    :Hlosses: list of (n_omics) lists, augmented list of
        marginal losses for H^(j).
    :Hgrads: list of (n_omics) lists, augmented list of
        gradient values in H^(j) (before update).


    Note
    ----
    See (Fevotte, 2011) and sklearn.decomposition.NMF source code for
    choice of parameters.
    """
    # W update with new values of Hs
    W_new = _update_W(W, omics, Hs, params["mu"])

    # Hs updates (either MU or Proximal)
    Hs_new = [0 for j in range(len(omics))]
    for j in range(len(omics)):
        Hs_new[j], Hgrads[j] = _update_H(
            Hs[j],
            W_new,
            omics[j],
            Betas[j],
            Y,
            params["gamma"],
            current_etas[j],
            params["lambda"],
            as_sklearn=as_sklearn,
            grad=True,
            H_grad=Hgrads[j],
        )

    if backtrack and not as_sklearn:
        # LineSearch for each H
        for j in range(len(omics)):
            Hlosses[j].append(
                _computeMargH(
                    omics[j],
                    Y,
                    W_new,
                    Hs_new[j],
                    Betas[j],
                    params["gamma"],
                    params["lambda"],
                    K_gp
                )
            )
            Hs_new[j], Hlosses[j], current_etas[j] = _linesearch(
                H_old=Hs[j],
                H=Hs_new[j],
                W=W_new,
                omic=omics[j],
                Beta=Betas[j],
                Y=Y,
                gamma=params["gamma"],
                lambdA=params["lambda"],
                current_eta=current_etas[j],
                H_loss=Hlosses[j],
                alpha=params["alpha"],
                sigma=params["sigma"],
                m_back=params["m_back"],
                max_iter_back=max_iter_back,
                K_gp=K_gp,
                verbose=verbose,
            )

    # Betas updates with new values of Hs
    # Compute each regression coef. of each component separately
    # and gather them in a unique vector
    Betas_new = [0 for j in range(len(omics))]
    for j in range(len(omics)):
        Betas_new[j] = np.array(
            [
                _update_Beta(
                    omics[j],
                    Hs_new[j][k, :],
                    Y[:, k],
                    params["gamma"],
                    Betas[j][k]
                ) for k in range(K)
            ]
        )
        # Put to zero all coefficients linked to components k when k > K_gp
        if K_gp < K:
            Betas_new[j][K_gp:] = 0

    return (
        W_new,
        Hs_new,
        Betas_new,
        current_etas,
        Hlosses,
        Hgrads,
    )


def _autograd_solver():
    """Another version of NMFProfiler solver.

    This solver is based on gradients automatically computed thanks to
    `autograd` python library.

    Note this feature has not been implemented so far.
    """
    raise Exception(
        "Feature not implemented yet. Please use 'analytical' solver."
    )


class NMFProfiler:
    r"""A multi-omics integration method for samples stratified in groups

    The goal of the method is to find relationships between OMICS
    corresponding to typical profiles of distinct groups of individuals. The
    objective is to find one decomposition for each omic, with a common
    contribution of individuals, in which latent factor matrices are sparse.

    The objective function
    :math:`\mathcal{F}
    (\mathbf{W},\mathbf{H}^{(1)},\ldots,\mathbf{H}^{(J)},\beta^{(1)},\ldots,\beta^{(J)})`
    is as follows:

    .. math::

        & \dfrac{1}{2}\left( \sum_{j=1}^J\| \mathbf{X}^{(j)} -
        \mathbf{WH}^{(j)} \|_F^2 \right)

        &+ \dfrac{\gamma}{2}\left( \sum_{j=1}^J\| \mathbf{Y} -
        \mathbf{X}^{(j)} \mathbf{H}^{(j)\top} \text{Diag}(\beta^{(j)})
        \|_F^2 \right)

        &+ \sum_{j=1}^{J} \lambda\|\mathbf{H}^{(j)}\|_1 +
        \dfrac{\mu}{2}\|\mathbf{W \|_F^2}

    Parameters
    ----------
    :omics: list of (n_omics) array-like of shape
            (n_samples x n_features_omicj).
        Omics datasets. (n_samples) is the number of samples and
        (n_features_omicj) the number of features of (omicj).
        WARNING: each (omicj) must contain the exact same samples
        in the same order.

    :y: vector of length (n_samples).
        Group to which each sample belongs (same order than the rows of omicj).

    :params: dict of length 7, optional.
        Contains, in this order, values for hyperparameters `gamma`, `lambda`,
        `mu` (from the objective function), for `eta` (when proximal
        optimization is used), and for `alpha`, `sigma`, `m_back` (for
        `linesearch()`).
        By default, gamma = 1e-2, lambda = 1e-3, mu = 1e-3, eta = 1,
        alpha = 2, sigma = 1e-9, and m_back = 1. In the objective function,
        `lambda` and `gamma` are additionally multiplied by (n_samples).

    :init_method: str, optional.
        Initialization method. One of {`'random2'`, `'random3'`, `'nndsvd2'`,
        `'nndsvd3s'`, `'nndsvd'`, `'nndsvda'`, `'nndsvdar'`}. Initializations
        are base on the `_initialize_nmf` function of the
        `sklearn.decomposition.NMF` module.
        In addition, for `'random2'` and `'random3'`, values are drawn
        from a standard Normal distribution (with 0 mean and standard deviation
        equal to 1).
        By default, `init_method = 'random2'`.
        See `_initialize_nmf()` for further information.

    :solver: str, optional.
        Solver type for the optimization problem. One of `'analytical'`
        (analytical differentiation) or `'autograd'` (automatic
        differentiation). Note the latter solver is not implemented in
        the current version, but should be released in future versions.
        By default, `solver = 'analytical'`.

    :as_sklearn: boolean, optional.
        If `True`, the solver uses MU updates. If `False`, it uses a proximal
        optimization strategy.
        By default, `as_sklearn = True`.

    :backtrack: boolean, optional.
        When `as_sklearn = False`, whether or not to perform Backtrack
        LineSearch.
        By default, `backtrack = False`.

    :max_iter_back: int, optional.
        When `max_iter_back = True`, maximum number of iterations for the
        Backtrack LineSearch.
        By default, `max_iter_back = 100`.

    :tol: float, optional.
        Tolerance for the stopping condition.
        By default, `tol = 1e-4`.

    :max_iter: int, optional.
        Maximum number of allowed iterations.
        By default, `max_iter = 1000`.

    :seed: int, optional.
        Random seed to ensure reproducibility of results.
        By default, seed = None.

    :verbose: boolean, optional.
        Verbose optimization process.
        By default, `verbose = False`.


    Attributes
    ----------
    :W: ndarray of shape (n_samples x K).
        Contributions of individuals in each latent component.

    :W_init: ndarray of shape (n_samples x K).
        Initial version of (W).

    :Hs: list of (n_omics) ndarrays of shape (K x n_features_omicj).
        Latent components Hj for (omicj).

    :Hs_init: list of (n_omics) ndarrays of shape (K x n_features_omicj).
        Initial version of (Hj).

    :Betas: list of (n_omics) ndarrays of shape (K x 1).
        Regression coefficients for the projection of individuals from (omicj)
        onto (Hj).

    :Betas_init: list of (n_omics) ndarrays of shape (K x 1).
        Initial version of (Betaj).

    :n_iter: int.
        Final number of iterations (up to convergence or maximum number of
        iterations is reached).

    :df_etas: `pd.dataFrame` of shape (n_iter+1, n_omics).
        Optimal values for parameter `eta` at each iteration.

    :df_errors: `pd.dataFrame` of shape (n_iter+1, 9).
        All error terms for each iteration and omic j.

    :df_ldaperf: `pd.DataFrame` of shape (n_iter+1, 13).
        All metrics linked to LDA at each iteration and omic j.

    :df_grads: `pd.DataFrame` of shape (n_iter+1, n_omics)
        Values of H^(j) gradients before being updated, at each
        iteration.

    :df_y: `pd.DataFrame` of shape (n, 2)
        Original levels in :y: as well as their associated
        integer.

    :runningtime: float.
        Running time of the method measured through `process_time()`.

    ... : all inputs passed to `NMFProfiler()`.


    References
    ----------
    C. Boutsidis and E. Gallopoulos. SVD based initialization: A head
    start for nonnegative matrix factorization. Pattern Recognition.
    Volume 41, Issue 4. 2008. Pages 1350-1362.
    https://doi.org/10.1016/j.patcog.2007.09.010.

    J. Leuschner, M. Schmidt, P. Fernsel, D. Lachmund, T. Boskamp, and
    P. Maass. Supervised non-negative matrix factorization methods for
    MALDI imaging applications. Bioinformatics.
    Volume 35. 2019. Pages 1940-1947
    https://doi.org/10.1093/bioinformatics/bty909.

    S. Zhang, C.-C. Liu, W. Li, H. Shen, P. W. Laird, and X. J. Zhou.
    Discovery of multi-dimensional modules by integrative analysis of
    cancer genomic data. Nucleic acids research.
    Volume 40, Issue 19. 2012. Pages 9379-9391.
    https://doi.org/10.1093/nar/gks725.

    A. Mercadie, E. Gravier, G. Josse, N. Vialaneix, and C. Brouard.
    NMFProfiler: A multi-omics integration method for samples stratified in
    groups. Preprint submitted for publication.

    Examples
    --------

    >>> import numpy as np
    >>> X1 = np.array([[1, 1.8, 1],
    >>>                [2, 3.2, 1],
    >>>                [1.5, 2.8, 1],
    >>>                [4.1, 0.7, 0.1],
    >>>                [5.01, 0.8, 0.1],
    >>>                [6.2, 0.9, 0.1]])
    >>> X2 = np.array([[2, 2.8, 2],
    >>>                [3, 4.2, 2],
    >>>                [2.5, 3.8, 2],
    >>>                [5.1, 1.7, 1.1],
    >>>                [6.01, 1.8, 1.1],
    >>>                [7.2, 1.9, 1.1]])
    >>> y = np.array([1, 1, 1, 0, 0, 0])
    >>> seed = 240805
    >>> from nmfprofiler import NMFProfiler
    >>> model = NMFProfiler(omics=[X1, X2], y=y, seed=seed)
    >>> res = model.fit()
    >>> print(res)
    >>> res.heatmap(obj_to_viz="W", height=10, width=10, path="")
    >>> model.barplot_error(height=6, width=15, path="")
    """

    def __init__(
        self,
        omics,
        y,
        params={
            "gamma": 1e-2,
            "lambda": 1e-3,
            "mu": 1e-3,
            "eta": 1.00,
            "alpha": 2,
            "sigma": 1e-9,
            "m_back": 1,
        },
        init_method="random2",
        solver="analytical",
        as_sklearn=True,
        backtrack=False,
        max_iter_back=100,
        tol=1e-4,
        max_iter=1000,
        seed=None,
        verbose=False,
    ):

        self.omics = omics
        self.y = y
        self.params = params
        self.init_method = init_method
        self.solver = solver
        self.as_sklearn = as_sklearn
        self.backtrack = backtrack
        self.max_iter_back = max_iter_back
        self.tol = tol
        self.max_iter = max_iter
        self.seed = seed
        self.verbose = verbose

    def __str__(self):
        """Briefly describe inputs and outputs of NMFProfiler."""
        print_statement = (
            f"NMFProfiler\n-----------\n\nAnalysis run on {len(self.omics)} "
            "datasets containing respectively "
            f"{*[self.omics[j].shape[1] for j in range(len(self.omics))], } "
            f"features measured on the same {self.omics[0].shape[0]} samples."
            f"\nSamples are splitted into {len(np.unique(self.y))} distinct"
            f" groups.\n\nNMFProfiler (as_sklearn = {self.as_sklearn}) "
            f"extracted {len(np.unique(self.y))} profiles "
            f"in {self.runningtime} seconds.\n\nFor more information, please "
            "refer to help() or GitLab page."
        )
        return print_statement

    def _update_params(self):
        """Adapt hyperparameters to the datasets analyzed.

        Hyperparameters lambda and gamma, used in the objective function,
        depend on (n_samples), the number of samples.
        This function will update them accordingly.
        """
        # Multiply lambda parameter by n_samples to get its final value
        self.updatedparams["lambda"] *= self.y.shape[0]

        # Multiply gamma parameter by n_samples to get its final value
        self.updatedparams["gamma"] *= self.y.shape[0]

    def _preprocess_data(self):
        """Pre-process datasets.

        Apply a min-max normalization and divide by the square root
        of the number of features.
        """
        # For each dataset
        for j in range(len(self.omics)):
            for i in range(self.omics[j].shape[1]):
                self.omics[j][:, i] = (
                    self.omics[j][:, i] - np.min(self.omics[j][:, i])
                ) / (
                    np.max(self.omics[j][:, i]) - np.min(self.omics[j][:, i])
                )
            self.omics[j] = (
                self.omics[j] * (1 / np.sqrt(self.omics[j].shape[1]))
            )

    def _initialize_w_h_beta(self):
        """Initialize matrices W, H^j and Beta^j.

        Several ways to intialize W, Hj.
        Betaj are initialized with 1s vectors.

        Note
        ----
        Based on _initialize_nmf of sklearn.decomposition.NMF.
        """
        # Extract K, the number of latent components, as equal to
        # the number of distinct groups in y
        K = len(np.unique(self.y))
        # For now, initialize K_gp, the number of latent components
        # dedicated to groups, identically to K
        K_gp = len(np.unique(self.y))

        # For W and Hj:
        # 1.0. Initialize H0s list
        H0s = [0 for j in range(len(self.omics))]
        # 1.1. Concatenate omics data sets
        omics = np.concatenate(self.omics, axis=1)
        # 1.2. Initialize using sklearn function
        if self.init_method == "random2":
            # 1.2a. Initialize W with both omics and Hj
            # with specific omic (random)
            W0, *_ = _initialize_nmf(
                X=omics,
                n_components=K,
                init="random",
                random_state=self.seed
            )
            for j in range(len(self.omics)):
                *_, H0s[j] = _initialize_nmf(
                    X=self.omics[j],
                    n_components=K,
                    init="random",
                    random_state=self.seed
                )
                del _
        elif self.init_method == "random3":
            # 1.2b. FOR IDENTICAL OMICS DATA SETS - Initialize W
            # with both omics, H1 with omic1 and other Hj as H1 (random)
            W0, H0s[0] = _initialize_nmf(
                X=self.omics[0],
                n_components=K,
                init="random",
                random_state=self.seed
            )
            for j in range(1, len(self.omics)):
                H0s[j] = H0s[0].copy()
        elif self.init_method == "nndsvd2":
            # 1.2c. Initialize W with both omics and Hj
            # with specific omic (nndsvd)
            W0, *_ = _initialize_nmf(
                X=omics,
                n_components=K,
                init="nndsvd",
                random_state=self.seed
            )
            for j in range(len(self.omics)):
                *_, H0s[j] = _initialize_nmf(
                    X=self.omics[j],
                    n_components=K,
                    init="nndsvd",
                    random_state=self.seed
                )
                del _
        elif self.init_method == "nndsvd3":
            # 1.2d. Initialize W with each omic then take the mean and
            # initialize Hj with specific omic (nndsvd)
            W_js = [0 for j in range(len(self.omics))]
            for j in range(len(self.omics)):
                W_js[j], H0s[j] = _initialize_nmf(
                    X=self.omics[j],
                    n_components=K,
                    init="nndsvd",
                    random_state=self.seed
                )
            W0 = (1 / len(self.omics)) * (sum(W_js))
            del W_js
        else:
            # 1.2e. Initialize both with all omics, using whatever method
            # available in _initialize_nmf(). See help.
            W0, H0 = _initialize_nmf(
                X=omics,
                n_components=K,
                init=self.init_method,
                random_state=self.seed
            )
            # 1.2e. Split H matrix
            if len(self.omics) == 2:
                indices_or_sections = [self.omics[0].shape[1]]
            else:
                indices_or_sections = [
                    self.omics[j].shape[1] for j in range(len(self.omics))
                ]
            H0s = np.split(
                ary=H0,
                indices_or_sections=indices_or_sections,
                axis=1
            )
            del H0

        # For Betas:
        Beta0s = [0 for j in range(len(self.omics))]
        for j in range(len(self.omics)):
            Beta0s[j] = np.repeat(1, K)
            # Put to zero all coefficients linked to component k when k > K_gp
            if K_gp < K:
                Beta0s[j][K_gp:] = 0

        return W0, H0s, Beta0s

    def fit(self):
        """Run NMFProfiler."""
        # Check hyperparameters and inputs
        _check_inputs_NMFProfiler(self)

        # Extract K, the number of latent components, as equal
        # to the number of distinct groups, U, in y
        K = len(np.unique(self.y))
        # For now, initialize K_gp, the number of latent components
        # dedicated to groups, identically to K
        K_gp = len(np.unique(self.y))

        # Turn y levels into integers
        if self.verbose:
            print("\nConverting y levels into integers...")
            print("Original levels: ", np.unique(self.y))
        y_init = deepcopy(self.y)
        num_levels = {}
        idx = 0
        for level in np.unique(self.y):
            if level not in num_levels:
                num_levels[level] = idx
                idx += 1
        self.y = np.array([num_levels[level] for level in self.y])
        if self.verbose:
            print("New levels: ", np.unique(self.y), "\n")

        # And automatically convert y into a one-hot encoded matrix Y
        encoder = OneHotEncoder(handle_unknown="ignore")
        Y = encoder.fit_transform(self.y.reshape(-1, 1)).toarray()

        # Pre-process datasets (with min-max and number of features)
        self._preprocess_data()

        # Initialize matrices
        W0, Hs_0, Betas_0 = self._initialize_w_h_beta()

        self.W_init = W0
        self.Hs_init = Hs_0
        self.Betas_init = Betas_0

        # Update lambda and gamma given sample size
        # - Make hard copy of self.params into self.updatedparams
        self.updatedparams = deepcopy(self.params)
        # - Update
        self._update_params()

        # Solve the minimization problem
        # ------------------------------

        # Create matrices and vectors to update using initialization
        # (and keep intact initialized matrices and vectors)
        W = deepcopy(W0)
        Hs = [deepcopy(Hs_0[j]) for j in range(len(self.omics))]
        Betas = [deepcopy(Betas_0[j]) for j in range(len(self.omics))]

        # Create lists of error terms to enrich iteratively
        (error, regul, nb_iters) = ([] for i in range(3))
        (
            margHs,
            gradHs,
            distorts,
            sparsitys,
            preds,
        ) = ([[] for j in range(len(self.omics))] for _ in range(5))

        # Create lists of LDA performance indicators to enrich iteratively
        (
            R2adjs,
            BICs,
            AICs,
            F_pvals,
        ) = ([[] for j in range(len(self.omics))] for _ in range(4))
        bets = [[[] for k in range(K)] for j in range(len(self.omics))]

        loss_init = _computeF(
            self.omics,
            Y,
            W0,
            Hs_0,
            Betas_0,
            self.updatedparams["mu"],
            self.updatedparams["lambda"],
            self.updatedparams["gamma"],
            K_gp,
            details=True,
        )
        error.append(loss_init[0])
        nb_iters.append(0)
        regul.append(loss_init[3])
        for j in range(len(self.omics)):
            distorts[j].append(loss_init[1][j])
            sparsitys[j].append(loss_init[2][j])
            preds[j].append(loss_init[4][j])

        # Keep track of marginal objective functions in Hj with
        # initial matrices (necessary for linesearch first execution)
        for j in range(len(self.omics)):
            margHs[j].append(
                _computeMargH(
                    self.omics[j],
                    Y,
                    W0,
                    Hs_0[j],
                    Betas_0[j],
                    self.updatedparams["gamma"],
                    self.updatedparams["lambda"],
                    K_gp,
                )
            )

        # LDAs with initial matrices
        regs_init = [0 for j in range(len(self.omics))]
        for j in range(len(self.omics)):
            regs_init[j] = sm.OLS(
                self.y,
                sm.add_constant(safe_sparse_dot(self.omics[j], Hs_0[j].T))
            ).fit()

        for j in range(len(self.omics)):
            for k in range(K):
                bets[j][k].append(regs_init[j].params[k+1])
            R2adjs[j].append(regs_init[j].rsquared_adj)
            BICs[j].append(regs_init[j].bic)
            AICs[j].append(regs_init[j].aic)
            F_pvals[j].append(regs_init[j].f_pvalue)

        # Show the initial global loss value
        if self.verbose:
            print("Error after initialization step: %f" % (error[0]))

        # To keep track of the choice of etas
        etas_init = [self.updatedparams["eta"] for j in range(len(self.omics))]
        etas = [[] for j in range(len(self.omics))]
        for j in range(len(self.omics)):
            etas[j].append(etas_init[j])

        # Begin the optimization
        start_time = process_time()
        for n_iter in range(1, self.max_iter + 1):

            # Solver

            # Analytical solver...
            if self.solver == "analytical":
                (
                    W,
                    Hs,
                    Betas,
                    current_etas,
                    margHs,
                    gradHs,
                ) = _analytic_solver(
                    self.omics,
                    Y,
                    W,
                    Hs,
                    Betas,
                    self.updatedparams,
                    current_etas=[
                        etas[j][-1] for j in range(len(self.omics))
                    ],
                    as_sklearn=self.as_sklearn,
                    backtrack=self.backtrack,
                    max_iter_back=self.max_iter_back,
                    Hlosses=margHs,
                    Hgrads=gradHs,
                    K=K,
                    K_gp=K_gp,
                    verbose=self.verbose,
                )

            # ... or Autograd solver
            else:
                W, Hs, Betas = _autograd_solver()

            # Keep track of optimal etas
            for j in range(len(self.omics)):
                etas[j].append(current_etas[j])

            # Compute the new loss as well as specific terms
            loss_ = _computeF(
                self.omics,
                Y,
                W,
                Hs,
                Betas,
                self.updatedparams["mu"],
                self.updatedparams["lambda"],
                self.updatedparams["gamma"],
                K_gp,
                details=True,
            )
            error.append(loss_[0])
            nb_iters.append(n_iter)
            regul.append(loss_[3])
            for j in range(len(self.omics)):
                distorts[j].append(loss_[1][j])
                sparsitys[j].append(loss_[2][j])
                preds[j].append(loss_[4][j])

            # Monitor the LDA part
            regs = [0 for j in range(len(self.omics))]
            for j in range(len(self.omics)):
                regs[j] = sm.OLS(
                    self.y,
                    sm.add_constant(safe_sparse_dot(self.omics[j], Hs[j].T))
                ).fit()

            for j in range(len(self.omics)):
                for k in range(K):
                    bets[j][k].append(regs[j].params[k+1])
                R2adjs[j].append(regs[j].rsquared_adj)
                BICs[j].append(regs[j].bic)
                AICs[j].append(regs[j].aic)
                F_pvals[j].append(regs[j].f_pvalue)

            # Every 10 iterations, if tol is still strictly positive and
            # verbose == True, compute the loss value
            if self.tol > 0 and n_iter % 10 == 0 and self.verbose:

                iter_time = process_time()
                print(
                    "Epoch %02d reached after %.3f seconds, error: %f"
                    % (n_iter, iter_time - start_time, error[-1])
                )

            # If the difference between losses at t and t-1
            # (divided by error_at_init) is smaller than threshold, stop algo.
            # Note the initial convergence criterion of scikit-learn was
            # (error[-2] - error[-1]) / error[0] < tol
            if (error[-2] - error[-1]) / error[-2] < self.tol:
                break

        end_time = process_time()
        self.runningtime = end_time - start_time

        # When converged, print global loss (IF not already shown prev.)
        # --------------------------------------------------------------
        if self.verbose and (self.tol == 0 or n_iter % 10 != 0):
            print(
                "Algorithm converged in %02d steps \
                 after %.3f seconds, error: %f"
                % (n_iter, end_time - start_time, error[-1])
            )

        # Warning if not converged (i.e. value of F not below tol)
        # but reached max_iter
        # --------------------------------------------------------
        if n_iter == self.max_iter and self.tol > 0:
            warnings.warn(
                "Maximum number of iterations %d reached. Increase "
                "it to improve convergence." % self.max_iter,
                ConvergenceWarning
            )

        # Store optimal values of matrices
        # --------------------------------
        self.n_iter = n_iter
        self.W = W
        self.Hs = Hs
        self.Betas = Betas

        # Keep track of final Hj gradients and build the Hj gradients matrix
        # (following up their evolution during optimization)
        # ------------------------------------------------------------------
        for j in range(len(self.omics)):
            gradHs[j].append(
                multi_dot([W.T, W, Hs[j]])
                + (
                    self.updatedparams["gamma"]
                    * multi_dot(
                        [
                            np.transpose(Betas[j][newaxis]),
                            Betas[j][newaxis],
                            Hs[j],
                            self.omics[j].T,
                            self.omics[j],
                        ]
                    )
                )
                - (
                    safe_sparse_dot(W.T, self.omics[j])
                    + (
                        self.updatedparams["gamma"]
                        * multi_dot(
                            [
                                np.transpose(Betas[j][newaxis]),
                                self.y[newaxis],
                                self.omics[j]
                            ]
                        )
                    )
                )
            )

        grads = np.array(
            [
                [
                    norm(i) ** 2 for i in gradHs[j]
                ] for j in range(len(self.omics))
            ]
        ).T
        self.df_grads = pd.DataFrame(
            grads,
            columns=[f'grad_H{j+1}' for j in range(len(self.omics))]
        )

        # Build the error terms matrix
        # ----------------------------
        error_terms = np.hstack(
            [
                np.vstack(nb_iters),
                np.array(distorts).T,
                np.array(sparsitys).T,
                np.vstack(regul),
                np.array(preds).T,
                np.vstack(error),
            ]
        )
        self.df_errors = pd.DataFrame(
            error_terms,
            columns=list(itertools.chain.from_iterable([
                ["iter"],
                [f"distort{j+1}" for j in range(len(self.omics))],
                [f"sparsity{j+1}" for j in range(len(self.omics))],
                ["regul"],
                [f"pred{j+1}" for j in range(len(self.omics))],
                ["loss"],
            ])),
        )

        # Build the LDA performance matrix
        # --------------------------------
        LDA_perf = np.vstack(nb_iters)
        for j in range(len(self.omics)):
            bets_j = np.array(bets[j]).T
            perf_j = np.array(
                [
                    R2adjs[j],
                    BICs[j],
                    AICs[j],
                    F_pvals[j],
                ]
            ).T
            LDA_perf = np.hstack(
                [LDA_perf, bets_j, perf_j]
            )
        self.df_ldaperf = pd.DataFrame(
            LDA_perf,
            columns=list(itertools.chain.from_iterable([
                ["iter"],
                list(itertools.chain.from_iterable([[
                    *[f"Comp.{k+1} coef (omic{j+1})" for k in range(K)],
                    f"R2 Adjusted (omic{j+1})",
                    f"BIC (omic{j+1})",
                    f"AIC (omic{j+1})",
                    f"F-statistic p-value (omic{j+1})"
                ] for j in range(len(self.omics))])),
            ])),
        )

        # Build the etas matrix
        # (following up etas evolution during optimization)
        # -------------------------------------------------
        self.df_etas = pd.DataFrame(
            np.array(etas).T,
            columns=[f"eta_omic{j+1}" for j in range(len(self.omics))]
        )

        # Build the correspondance matrix between
        # original levels and their associated integer in y
        # -------------------------------------------------
        self.df_y = pd.DataFrame(
            {"Original_y": y_init,
             "Recoded_y": self.y}
        )

        return self

    def predict(self, new_ind, verbose=False):
        """Predict the group of a new sample, based on its projection onto
        signatures matrices.

        Params
        ------
        :new_ind: list. List of arrays containing values of
            features from omicj for a new sample.

        Values
        ------
        :group: list. Predicted group (one of 0 or 1) for the new sample
            in each omic.
        :projs: list of arrays. Projection onto each Hj matrix
        """
        # Initialize projection list and compute
        projs = []
        for j in len(new_ind):
            # Convert to right format
            new_ind_Xj = new_ind[j][newaxis]

            # Compute projections of the new samples onto dictionary matrices
            projs.append(safe_sparse_dot(new_ind_Xj, self.Hs[j].T))

        # For each omic, find which component gave the highest score
        group = [projs[j].argmax() for j in len(new_ind)]

        # Compute global group value
        group_value = int(np.average(group))
        if verbose:
            print(
                f"Profile of this new sample resembles \
                  profile of group {group_value}."
            )

        res = {"group": group, "projs": projs}

        return res

    def barplot_error(self, width, height, path):
        """Visualize of the final error terms.

        Params
        ------
        :width: int. Width of the figure (in `units` by default).
        :height: int. Height of the figure (in `units` by default).
        :path: str. Location to save the figure.

        Values
        ------
        Return a barplot of the different error terms.
        """
        J = len(self.omics)
        data_barplot = np.array([
            [
                *[f"reconstruction omic{j+1}" for j in range(J)],
                *[f"l1 penalty on H{j+1}" for j in range(J)],
                "l2 penalty on W",
                *[f"supervised part omic{j+1}" for j in range(J)],
            ],
            self.df_errors.iloc[-1, 1:-1].tolist(),
        ]).T
        df_bar = pd.DataFrame(data_barplot, columns=["part", "value"])
        df_bar["value"] = df_bar["value"].astype(float)

        plt.figure(figsize=(width, height))
        g = sns.barplot(data=df_bar, x="part", y="value")
        g.set(xlabel=None)
        plt.savefig(str(path + "BarplotErrors.png"))
        plt.show()

    def evolplot(self, obj_to_check, width, height):
        """Visualize the evolution of either etas values or gradients along
        the optimization process.

        Params
        ------
        :obj_to_check: str. One of {`'etas'`, `'gradients'`}.
        :width: int, width of the figure (in `units` by default).
        :height: int, height of the figure (in `units` by default).

        Values
        ------
        Return a lineplot.
        """
        temppalette = ["blue", "orange", "green", "pink", "yellow", "red"]

        if obj_to_check == "etas":
            plt.figure(figsize=(width, height))
            sns.lineplot(data=self.df_etas,
                         palette=temppalette[0:self.df_etas.shape[1]])
            plt.show()

        elif obj_to_check == "gradients":
            plt.figure(figsize=(width, height))
            sns.lineplot(data=self.df_grads,
                         palette=temppalette[0:self.df_etas.shape[1]])
            plt.show()

        else:
            raise Exception(
                "Cannot plot this object, please change 'obj_to_check' input."
                " Only 'df_etas' and 'df_gradients' outputs "
                "from NMFProfiler can be plotted with this method."
            )

    def heatmap(self, obj_to_viz, width, height, path, omic_number=None):
        """Visualize any matrix of X^j, W, H^j with a heatmap.

        Params
        ------
        :obj_to_viz: str. One of {`'omic'`, `'W'`, `'H'`}.
        :omic_number: int. Number from 1 to J (max. number of omics).
        :width: int. Width of the figure (in units by default).
        :height: int. Height of the figure (in units by default).
        :path: str. Location to save the figure.

        Values
        ------
        Returns a heatmap.
        """
        plt.figure(figsize=(width, height))

        if obj_to_viz == "W":
            sns.heatmap(pd.DataFrame(self.W), cmap="viridis")
        elif obj_to_viz == "omic":
            sns.heatmap(
                pd.DataFrame(self.omics[(omic_number-1)]),
                cmap="viridis"
            )
        elif obj_to_viz == "H":
            sns.heatmap(pd.DataFrame(self.Hs[(omic_number-1)]), cmap="viridis")
        else:
            raise Exception(
                "Cannot plot this object, please change 'obj_to_viz' input."
                " Only 'omic', 'W' and 'H' outputs "
                "from NMFProfiler can be plotted with this method."
            )

        if obj_to_viz == "W":
            plotname = str(path + obj_to_viz + "_Heatmap.png")
        else:
            plotname = str(
                path + obj_to_viz + str(omic_number) + "_Heatmap.png"
            )

        plt.savefig(plotname)
        plt.show()
