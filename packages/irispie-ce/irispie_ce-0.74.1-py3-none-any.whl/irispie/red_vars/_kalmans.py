r"""
Kalman filter inlay
"""


#[

from __future__ import annotations

import numpy as _np
import documark as _dm

from .. import dates as _dates
from ..fords import kalmans as _kalmans
from ..dataslates.main import Dataslate

#]


def mixin(klass: type, ) -> type:
    r"""
    Inlay Kalman filter methods in the class
    """
    #[
    klass.kalman_filter = kalman_filter
    return klass
    #]


#--------------------------------------------------------------------------------
# Functions to be used as methods in RedVAR class
#--------------------------------------------------------------------------------


@_dm.reference(category="filtering", )
def kalman_filter(
    self,
    input_db: Databox,
    span: Iterable[Period],
    #
    residuals_from_data: bool = False,
    #
    num_variants: int | None = None,
    prepend_initial: bool = False,
    append_terminal: bool = False,
    #
    **kwargs,
):
    r"""
    """
    slatable = self.slatable_for_kalman_filter(
        residuals_from_data=residuals_from_data,
    )
    #
    long_span = _dates.long_span_from_short_span(span, max_lag=-self.order, )
    num_variants = self.resolve_num_variants_in_context(num_variants, )
    work_db = input_db.shallow()
    input_ds = Dataslate.from_databox_for_slatable(
        slatable, work_db, long_span,
        num_variants=num_variants,
        prepend_initial=prepend_initial,
        append_terminal=append_terminal,
        clip_data_to_base_span=True,
    )
    #
    columns_to_run = range(self.order, input_ds.num_periods, )
    return _kalmans.kalman_filter(
        self, input_ds, long_span,
        generate_period_system=_generate_period_system,
        generate_period_data=_generate_period_data,
        presimulate_exogenous_impact=None,
        num_variants=num_variants,
        initialize="data",
        columns_to_run=columns_to_run,
        **kwargs,
    )


#--------------------------------------------------------------------------------


def _generate_period_system(
    t: int,
    #
    solution_v: Solution,
    y1_array: _np.ndarray,
    **kwargs,
    # std_u_array: _np.ndarray,
    # std_w_array: _np.ndarray,
    # all_v_impact: Sequence[_np.ndarray | None] | None,
) -> tuple[_np.ndarray, ...]:
    r"""
    """
    #[
    T = solution_v.T
    P = solution_v.P
    K = solution_v.K
    inx_y = ~_np.isnan(y1_array[:, t], )
    Z = solution_v.Z[inx_y, :]
    H = solution_v.H[inx_y, :]
    D = solution_v.D[inx_y]
    U = None
    cov_u = solution_v.cov_u
    cov_w = solution_v.cov_w
    exogenous_impact = None # all_v_impact[t] if all_v_impact is not None else None
    return T, P, K, Z, H, D, cov_u, cov_w, exogenous_impact, U,
    #]


def _generate_period_data(
    t,
    #
    y_array: _np.ndarray,
    u_array: _np.ndarray,
    v_array: _np.ndarray,
    w_array: _np.ndarray,
) -> tuple[_np.ndarray, ...]:
    r"""
    """
    #[
    inx_y = ~_np.isnan(y_array[:, t], )
    y = y_array[inx_y, t]
    u = u_array[:, t]
    v = v_array[:, t]
    w = w_array[:, t]
    return y, u, v, w, inx_y.tolist(),
    #]

