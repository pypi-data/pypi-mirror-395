r"""
Implement Squidable for Simultaneous models
"""

#[

from __future__ import annotations

from ..fords.descriptors import Squidable

#]


def mixin(klass: type, ) -> type:
    r"""
    """
    #[
    klass.get_squidable = get_squidable
    return klass
    #]


#-------------------------------------------------------------------------------
# Functions to be used as methods in Simultaneous class
#-------------------------------------------------------------------------------


def get_squidable(self, ) -> Squidable:
    r"""
    """
    #[
    return Squidable(
        solution_vectors=self.solution_vectors,
        shock_qid_to_std_qid=self.shock_qid_to_std_qid,
    )
    #]


#-------------------------------------------------------------------------------

