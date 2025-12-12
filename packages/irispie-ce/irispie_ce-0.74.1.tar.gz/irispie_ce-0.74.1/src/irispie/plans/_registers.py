"""
Mixin for plan registers
"""


#[

from __future__ import annotations

import functools as _ft

from .. import wrongdoings as _wrongdoings

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable, NoReturn, Any, Iterable, EllipsisType

#]


def mixin(klass: type, ) -> type:
    r"""
    Mix the register properties and methods into the class
    """
    #[
    klass.get_register_by_name = get_register_by_name
    klass._initialize_registers = _initialize_registers
    klass._resolve_register_names = staticmethod(_resolve_register_names)
    #
    return klass
    #]


#-------------------------------------------------------------------------------
# Functions to be used as methods in plan classes
#-------------------------------------------------------------------------------


def _initialize_registers(
    self,
    plannable,
    create_default_value: Callable,
) -> None:
    """
    """
    self._registers = plannable.registers
    self._user_methods = plannable.user_methods
    for r in self._registers:
        register = Register(r, )
        names_in_register = getattr(plannable, f"can_be_{r}", )
        for n in names_in_register:
            register[n] = create_default_value()
        setattr(self, f"can_be_{r}", tuple(register.keys()))
        setattr(self, f"_{r}_register", register)

def get_register_by_name(self, name: str, ) -> dict[str, Any]:
    """ """
    full_name = f"_{name}_register"
    return getattr(self, full_name, )


def _resolve_register_names(
    register: dict | None,
    names: Iterable[str] | str | EllipsisType,
) -> tuple[str] | NoReturn:
    """
    """
    keys = tuple(register.keys()) if register else ()
    if names is Ellipsis:
        names = keys
    elif isinstance(names, str):
        names = (names, )
    else:
        names = tuple(names)
    register.validate_register_names(names, )
    return names


#-------------------------------------------------------------------------------


class Register(dict, ):
    r"""
    """
    #[

    def __init__(self, name: str, ) -> None:
        r"""
        """
        super().__init__()
        self.name = name

    def validate_register_names(
        self,
        names: Iterable[str],
    ) -> None | NoReturn:
        r"""
        """
        keys = tuple(self.keys()) if self else ()
        invalid = tuple(n for n in names if n not in keys)
        if invalid:
            message = (f"These names cannot be {self.name}:", ) + invalid
            raise _wrongdoings.IrisPieCritical(message, )

    #]

