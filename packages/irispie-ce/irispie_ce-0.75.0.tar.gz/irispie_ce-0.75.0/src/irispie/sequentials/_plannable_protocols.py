"""
Implement SimulationPlannableProtocol
"""


#[
from __future__ import annotations
#]


class _SimulationPlannable:
    """
    """
    #[

    def __init__(
        self,
        sequential,
        **kwargs,
    ) -> None:
        r"""
        """
        self.registers = (
            "exogenized",
        )
        self.user_methods = (
            "exogenize",
        )
        self.can_be_exogenized \
            = tuple(set(
                i.lhs_name for i in sequential._invariant.explanatories
                if not i.is_identity
            ))


class Inlay:
    r"""
    """
    #[

    def get_simulation_plannable(self, **kwargs, ) -> _SimulationPlannable:
        r"""
        """
        return _SimulationPlannable(self, **kwargs, )

    #]

