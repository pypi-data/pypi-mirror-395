"""
Initialize median and MSE matrix for alpha vector
"""


#[

from __future__ import annotations

import numpy as _np

from ..incidences import main as _incidences
from .solutions import left_div
from . import covariances as _covariances

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from numbers import Real
    from typing import Literal
    from ..dataslates.main import Dataslate
    from .solutions import Solution
    from .descriptors import SolutionVectors

#]


_DEFAULT_DIFFUSE_SCALE = 1e8


#-------------------------------------------------------------------------------
# Initializers for asymptotic initial conditions
#-------------------------------------------------------------------------------


def _approx_diffuse(
    solution: Solution,
    custom_diffuse_scale: Real | None = None,
) -> tuple[Real, _np.ndarray | None]:
    """
    """
    #[
    diffuse_scale = custom_diffuse_scale or _DEFAULT_DIFFUSE_SCALE
    unknown_init_impact = None
    return diffuse_scale, unknown_init_impact
    #]


def _fixed_unknown(
    solution: Solution,
    custom_diffuse_scale: Real | None = None,
) -> tuple[Real, _np.ndarray | None]:
    """
    """
    #[
    diffuse_scale = 0
    unknown_init_impact = (
        _np.eye(solution.num_xi, solution.num_unit_roots, )
        if solution.num_unit_roots else None
    )
    return diffuse_scale, unknown_init_impact,
    #]


def _fixed_zero(
    solution: Solution,
    custom_diffuse_scale: Real | None = None,
) -> tuple[Real, _np.ndarray | None]:
    """
    """
    #[
    diffuse_scale = 0
    unknown_init_impact = None
    return diffuse_scale, unknown_init_impact,
    #]


_RESOLVE_DIFFUSE = {
    "approx_diffuse": _approx_diffuse,
    "fixed_unknown": _fixed_unknown,
    "fixed_zero": _fixed_zero,
}


def initialize_asymptotic(
    solution: Solution,
    diffuse_method: Literal["approx_diffuse", "fixed_unknown", "fixed_zero", ] = "fixed_unknown",
    diffuse_scale: Real | None = None,
    **kwargs,
) -> tuple[_np.ndarray, _np.ndarray, _np.ndarray, ]:
    r"""
    Return median and MSE matrix for initial alpha, and the impact of fixed
    unknowns on initial alpha
    """
    #[
    diffuse_func = _RESOLVE_DIFFUSE[diffuse_method]
    diffuse_scale, unknown_init_impact = diffuse_func(solution, diffuse_scale, )
    init_med = _initialize_med(solution, )
    init_mse = _initialize_mse(solution, diffuse_scale, )
    return init_med, init_mse, unknown_init_impact,
    #]


def _initialize_med(solution: Solution, ) -> _np.ndarray:
    """
    Solve alpha_stable = Ta_stable @ alpha_stable + Ka_stable for alpha_stable
    and return alpha with 0s for unstable elements
    """
    #[
    num_alpha = solution.num_alpha
    num_unit_roots = solution.num_unit_roots
    num_stable = solution.num_stable
    Ta_stable = solution.Ta_stable
    Ka_stable = solution.Ka_stable
    init_med = _np.zeros((num_alpha, ), dtype=float, )
    #
    T = _np.eye(num_stable, dtype=float, ) - Ta_stable
    init_med_stable = left_div(T, Ka_stable, )
    init_med[num_unit_roots:] = init_med_stable
    return init_med
    #]


def _initialize_mse(
    solution: Solution,
    diffuse_scale: Real | None = None,
) -> _np.ndarray:
    """
    """
    #[
    init_mse = _covariances.get_cov_alpha_00(solution, solution.cov_u, )
    if diffuse_scale:
        num_unit_roots = solution.num_unit_roots
        init_mse[:num_unit_roots, :num_unit_roots] = \
            _initialize_mse_unstable_approx_diffuse(solution, init_mse, diffuse_scale, )
    init_mse = _covariances.symmetrize(init_mse, )
    return init_mse
    #]


def _initialize_mse_unstable_approx_diffuse(
    solution: Solution,
    init_mse: _np.ndarray,
    diffuse_scale: Real | None = None,
) -> _np.ndarray:
    """
    """
    #[
    num_unit_roots = solution.num_unit_roots
    num_alpha = solution.num_alpha
    cov_u = solution.cov_u
    base_cov = (
        init_mse[num_unit_roots:, num_unit_roots:] if num_alpha
        else (cov_u if cov_u.size else _np.ones((1, 1, ), dtype=float, ))
    )
    scale = _mean_of_diag(base_cov, ) * diffuse_scale
    return scale * _np.eye(num_unit_roots, dtype=float, )
    #]


def _mean_of_diag(x: _np.ndarray, ) -> Real:
    """
    """
    return _np.mean(_np.diag(x, ), )



#-------------------------------------------------------------------------------
# Initializers from data
#-------------------------------------------------------------------------------


def initialize_from_data(*args, **kwargs, ) -> tuple[_np.ndarray, _np.ndarray, _np.ndarray, ]:
    r"""
    """
    #[
    init_med = get_true_init_xi_from_data(*args, **kwargs, )
    num_alpha = init_med.size
    init_mse = _np.zeros((num_alpha, num_alpha, ), dtype=float, )
    unknown_init_impact = None
    return init_med, init_mse, unknown_init_impact,
    #]


def get_true_init_xi_from_data(
    data_array: _np.ndarray,
    solution_vectors: SolutionVectors,
    first_column: int,
    **kwargs,
) -> _np.ndarray:
    r"""
    """
    #[
    init_xi = _get_init_xi_from_data(
        data_array,
        solution_vectors.transition_variables,
        first_column,
    )
    _zero_false_init_xi(init_xi, solution_vectors.true_initials, )
    return init_xi
    #]


def _get_init_xi_from_data(
    maybelog_working_data: _np.ndarray,
    transition_solution_vector: Iterable[Token, ...],
    first_column: int,
) -> _np.ndarray:
    """
    """
    #[
    init_xi_rows, init_xi_columns = _incidences.rows_and_columns_from_tokens(
        transition_solution_vector,
        first_column - 1,
    )
    return maybelog_working_data[init_xi_rows, init_xi_columns]
    #]


def _zero_false_init_xi(
    init_xi: _np.ndarray,
    true_initials: Iterable[bool, ...],
) -> None:
    #[
    false_initials = [ (not i) for i in true_initials ]
    init_xi[false_initials, ...] = 0
    #]


