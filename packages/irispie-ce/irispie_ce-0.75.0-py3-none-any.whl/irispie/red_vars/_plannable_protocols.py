r"""
Implement SimulationPlannableProtocol
"""


#[

from __future__ import annotations

from .. import quantities as _quantities

from ..quantities import (
    TRANSITION_VARIABLE,
    TRANSITION_SHOCK,
    ANTICIPATED_SHOCK_VALUE,
    ENDOGENOUS_VARIABLE,
    PARAMETER,
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .main import Simultaneous
    from ..quantities import QuantityKind

#]


def mixin(klass: type, ) -> type:
    r"""
    Inlay plannable protocol methods in the class
    """
    #[
    klass.get_simulation_plannable = get_simulation_plannable
    return klass
    #]


#-------------------------------------------------------------------------------
# Functions to be used as methods in RedVAR class
#-------------------------------------------------------------------------------


def get_simulation_plannable(self, ) -> _SimulationPlannable:
    """
    """
    return _SimulationPlannable(model=self, )


#-------------------------------------------------------------------------------


class _SimulationPlannable:
    r"""
    """
    #[

    def __init__(
        self,
        model,
    ) -> None:
        r"""
        """
        self.registers = (
            "conditioned",
        )
        self.user_methods = (
            "condition",
        )
        self.can_be_conditioned = model.get_names(kind=TRANSITION_VARIABLE, ) 

    #]

