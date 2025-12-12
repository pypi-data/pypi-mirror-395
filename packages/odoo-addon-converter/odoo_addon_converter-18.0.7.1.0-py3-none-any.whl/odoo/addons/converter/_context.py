##############################################################################
#
#    Converter Odoo module
#    Copyright © 2025 XCG SAS <https://orbeet.io/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import abc
import inspect
from collections.abc import Callable, Iterable, Mapping
from typing import Any

from odoo import models
from odoo.tools import frozendict
from typing_extensions import override


class Computed(abc.ABC):
    @abc.abstractmethod
    def compute(
        self,
        key: str,
        parent: Mapping,
        instance: models.BaseModel,
        message: Mapping | None,
    ) -> Any:
        pass


class CustomComputed(Computed):
    Fn = (
        # key|parent|instance|message
        Callable[[str | Mapping | models.BaseModel | Mapping | None], Any]
        # key, parent|instance|message
        | Callable[[str, Mapping | models.BaseModel | Mapping | None], Any]
        # parent, instance|message
        | Callable[[Mapping, models.BaseModel | Mapping | None], Any]
        # key, parent, instance|message
        | Callable[[str, Mapping, models.BaseModel | Mapping | None], Any]
        # key, instance, message
        | Callable[[str, models.BaseModel, Mapping | None], Any]
        # key, parent, instance, message
        | Callable[[str, Mapping, models.BaseModel, Mapping | None], Any]
    )

    def __init__(self, compute: Fn):
        sig = inspect.Signature.from_callable(compute)
        self._parameters = sig.parameters
        self._keyparam = "key" in sig.parameters
        self._parentparam = "parent" in sig.parameters
        self._instanceparam = "instance" in sig.parameters
        self._messageparam = "message" in sig.parameters
        self._compute = compute

    def compute(
        self,
        key: str,
        parent: Mapping,
        instance: models.BaseModel,
        message: Mapping | None,
    ) -> Any:
        args: list[Any] = []
        if self._keyparam:
            args.append(key)
        if self._parentparam:
            args.append(parent)
        if self._instanceparam:
            args.append(instance)
        if self._messageparam:
            args.append(message)
        return self._compute(*args)


class InstanceAttr(Computed):
    def __init__(self, name: str):
        self._name = name

    def compute(
        self,
        key: str,
        parent: Mapping,
        instance: models.BaseModel,
        message: Mapping | None,
    ) -> Any:
        if instance is None:
            return None
        return getattr(instance, self._name)


Context = Mapping[str, Any]


class Inherited(Computed):
    def __init__(self, name: str | None):
        self._name = name

    @override
    def compute(
        self,
        key: str,
        parent: Mapping,
        instance: models.BaseModel,
        message: Mapping | None,
    ) -> Any:
        if self._name:
            return parent[self._name]
        return parent[key]


class ContextBuilder:
    def __init__(
        self,
        variables: Mapping[str, Any] = frozendict(),
        inherit: Iterable[str] = (),
    ):
        self._variables: dict[str, Any] = dict(variables)
        # store inherit set as a list for faster iterations
        self._inherit: Iterable[str] = tuple(set(inherit))

    @staticmethod
    def instance_attr(name: str) -> Computed:
        """Get a given attribute of the current instance"""
        return InstanceAttr(name)

    @staticmethod
    def instance_id():
        """Get the current instance id"""
        return ContextBuilder.instance_attr("id")

    @staticmethod
    def from_parent(name: str) -> Computed:
        """Get a named value from the parent context."""
        return Inherited(name)

    @staticmethod
    def from_message(name: str) -> Computed:
        """Inherits a single value from the message value."""
        return CustomComputed(lambda message: message[name])

    inherit: Computed = Inherited(None)
    """Inherits a single value from the parent context.

    ```
    { "varname": ContextBuilder.inherit }
    ```

    is equivalent to:
    ```
    { "varname": ContextBuilder.from_parent("varname") }
    ```
    """

    @staticmethod
    def const(value: Any) -> Any:
        """A constant value"""
        return value

    @staticmethod
    def computed(compute: CustomComputed.Fn) -> Computed:
        """Compute a value.

        The given function may have one of several of the following parameters:
        - key: the variable name in the new context
        - parent: the parent context
        - instance: the current instance, if exists
        - message: the current message, if exists
        """
        return CustomComputed(compute)

    def inherited(self) -> Iterable[str]:
        keys = []
        match self._inherit:
            case [*items]:
                keys.extend(items)
            case _:
                pass

        for key, value in self._variables.items():
            if isinstance(value, Inherited):
                if value._name is None:
                    keys.append(key)
                else:
                    keys.append(value._name)

        return keys

    def inherit_if_missing(self, keys):
        """Add inherited keys to the context"""

        self._inherit = tuple(
            set(self._inherit).union(set(keys).difference(self._variables.keys()))
        )

    def _build(
        self, parent: Context, instance: models.BaseModel, message: Mapping | None
    ) -> Context:
        ctx: dict[str, Any] = {}

        if self._inherit is True:
            ctx.update(parent)
        elif self._inherit is False:
            pass
        else:
            for key in self._inherit:
                ctx[key] = parent[key]

        for key, value in self._variables.items():
            if isinstance(value, Computed):
                ctx[key] = value.compute(key, parent, instance, message)
            else:
                ctx[key] = value

        return ctx


def build_context(
    builder: ContextBuilder | None,
    parent: Context,
    instance: models.BaseModel,
    message: Mapping | None,
):
    if builder:
        return builder._build(parent, instance, message)

    return parent
