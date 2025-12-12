r"""
Kalman filter inlay
"""


#[

from __future__ import annotations

import numpy as _np
import documark as _dm

from ..dataslates.main import Dataslate
from ..fords import shock_simulators as _shock_simulators
from ..fords import kalmans as _kalmans

#]


# TODO: Create Kalmanable protocol


def mixin(klass: type, ) -> type:
    r"""
    Inlay Kalman filter methods in the class
    """
    #[
    klass.kalman_filter = kalman_filter
    return klass
    #]


#--------------------------------------------------------------------------------
# Functions to be used as methods in Simultaneous class
#--------------------------------------------------------------------------------


@_dm.reference(category="filtering", )
def kalman_filter(
    self,
    input_db: Databox,
    span: Iterable[Period],
    #
    shocks_from_data: bool = False,
    stds_from_data: bool = False,
    parameters_to_output: bool = False,
    #
    num_variants: int | None = None,
    prepend_initial: bool = False,
    append_terminal: bool = False,
    #
    **kwargs,
):
    r"""
················································································

==Run Kalman filter on a model using time series data==

Executes a Kalman filter on a model, compliant with `KalmanFilterableProtocol`,
using time series observations from the input Databox. This method enables state
estimation and uncertainty quantification in line with the model's dynamics and
the time series data.

kalman_output = self.kalman_filter(
    input_db,
    span,
    diffuse_scale=None,
    return_=("predict", "update", "smooth", "predict_err", "predict_mse_obs", ),
    return_predict=True,
    return_update=True,
    return_smooth=True,
    return_predict_err=True,
    return_predict_mse_obs=True,
    rescale_variance=False,
    likelihood_contributions=True,
    shocks_from_data=False,
    stds_from_data=False,
    prepend_initial=False,
    append_terminal=False,
    deviation=False,
    check_singularity=False,
    unpack_singleton=True,
    return_info=False,
)

kalman_output, info = self.kalman_filter(
    ...
    return_info=True,
)


### Input arguments ###


???+ input "self"
    Simultaneous model used to run the Kalman filter.

???+ input "input_db"
    A Databox containing time series data to be used for filtering.

???+ input "span"
    A date span over which the filtering process is executed based on the
    measurement time series.

???+ input "diffuse_scale"
    A real number or `None`, specifying the scale factor for the diffuse
    initialization. If `None`, the default value is used.

???+ input "return_"
    An iterable of strings indicating which steps' results to return:
    "predict", "update", "smooth".

???+ input "return_predict"
    If `True`, return prediction step results.

???+ input "return_update"
    If `True`, return update step results.

???+ input "return_smooth"
    If `True`, return smoothing step results.

???+ input "rescale_variance"
    If `True`, rescale all variances by the optimal variance scale factor
    estimated using maximum likelihood after the filtering process.

???+ input "likelihood_contributions"
    If `True`, return the contributions of individual periods to the overall
    (negative) log likelihood.

???+ input "shocks_from_data"
    If `True`, use possibly time-varying shock values from the data; these
    values are interpreted as the medians (means) of the shocks. If `False`,
    zeros are used for all shocks.

???+ input "stds_from_data"
    If `True`, use possibly time-varying standard deviation values from the
    data. If `False`, currently assigned constant values are used for the
    standard deviations of all shocks.

???+ input "prepend_initial"
    If `True`, prepend observations to the resulting time series to cover
    initial conditions based on the model's maximum lag. No measurement
    observations are used in these initial time periods (even if some are
    available in the input data).

???+ input "append_terminal"
    If `True`, append observations to the resulting time series to cover
    terminal conditions based on the model's maximum lead. No measurement
    observations are used in these terminal time periods (even if some are
    available in the input data).

???+ input "deviation"
    If `True`, the constant vectors in transition and measurement equations are
    set to zeros, effectively running the Kalman filter as deviations from
    steady state (a balanced-growth path)

???+ input "check_singularity"
    If `True`, check the one-step ahead MSE matrix for the measurement variables
    for singularity, and throw a `SingularMatrixError` exception if the matrix
    is singular.

???+ input "unpack_singleton"
    If `True`, unpack `out_info` into a plain dictionary for models with a
    single variant.

???+ input "return_info"
    If `True`, return additional information about the Kalman filtering process.


### Returns ###


???+ returns "kalman_output"
    A Databox containing some of the following items (depending on the user requests):

    | Attribute         | Type       | Description
    |-------------------|---------------------------------------------------
    | `predict_med`     | `Databox`  | Medians from the prediction step
    | `predict_std`     | `Databox`  | Standard deviations from the prediction step
    | `predict_mse_obs` | `list`     | Mean squared error matrices for the prediction step of the available observations of measurement variables
    | `update_med`      | `Databox`  | Medians from the update step
    | `update_std`      | `Databox`  | Standard deviations from the update step
    | `predict_err`     | `Databox`  | Prediction errors
    | `smooth_med`      | `Databox`  | Medians from the smoothing step
    | `smooth_std`      | `Databox`  | Standard deviations from the smoothing step


???+ returns "out_info"
    A dictionary containing additional information about the filtering process,
    such as log likelihood and variance scale. For models with multiple
    variants, `out_info` is a list of such dictionaries. If
    `unpack_singleton=False`, also `out_info` is a one-element list
    containing the dictionary for singleton models, too.

················································································
    """
    slatable = self.slatable_for_kalman_filter(
        shocks_from_data=shocks_from_data,
        stds_from_data=stds_from_data,
        parameters_to_output=parameters_to_output,
    )
    #
    num_variants = self.resolve_num_variants_in_context(num_variants, )
    work_db = input_db.shallow()
    input_ds = Dataslate.from_databox_for_slatable(
        slatable, work_db, span,
        num_variants=num_variants,
        prepend_initial=prepend_initial,
        append_terminal=append_terminal,
        clip_data_to_base_span=True,
    )
    #
    return _kalmans.kalman_filter(
        self, input_ds, span,
        generate_period_system=_generate_period_system,
        generate_period_data=_generate_period_data,
        presimulate_exogenous_impact=(
            _shock_simulators.simulate_triangular_anticipated_shock_values
            if shocks_from_data else None
        ),
        num_variants=num_variants,
        **kwargs,
    )


#--------------------------------------------------------------------------------


def _generate_period_system(
    t: int,
    #
    solution_v: Solution,
    y1_array: _np.ndarray,
    std_u_array: _np.ndarray,
    std_w_array: _np.ndarray,
    all_v_impact: Sequence[_np.ndarray | None] | None,
) -> tuple[_np.ndarray, ...]:
    """
    """
    #[
    T = solution_v.Ta
    P = solution_v.Pa
    K = solution_v.Ka
    inx_y = ~_np.isnan(y1_array[:, t], )
    Z = solution_v.Za[inx_y, :]
    H = solution_v.H[inx_y, :]
    D = solution_v.D[inx_y]
    U = solution_v.Ua
    cov_u = _np.diag(std_u_array[:, t]**2, )
    cov_w = _np.diag(std_w_array[:, t]**2, )
    v_impact = all_v_impact[t] if all_v_impact is not None else None
    return T, P, K, Z, H, D, cov_u, cov_w, v_impact, U,
    #]


def _generate_period_data(
    t,
    y_array: _np.ndarray,
    u_array: _np.ndarray,
    v_array: _np.ndarray,
    w_array: _np.ndarray,
) -> tuple[_np.ndarray, ...]:
    """
    """
    #[
    inx_y = ~_np.isnan(y_array[:, t], )
    y = y_array[inx_y, t]
    u = u_array[:, t]
    v = v_array[:, t]
    w = w_array[:, t]
    return y, u, v, w, inx_y.tolist(),
    #]

