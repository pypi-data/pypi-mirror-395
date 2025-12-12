##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020, 2025 XCG SAS <https://orbeet.io/>
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

"""Converter is a utility class that makes conversion very easy between
Odoo records & JSON dicts. It's very fast and extendable and convert both ways.

Supports aggregates of the form (simplified example JSON-schemas)::
    {"type": "object", "properties": { "items": { "type": "array", "items": {
        "type": "object", "properties": {
            "data": {"oneOf": [{"$ref": "user.json"}, {"$ref": "s2.json"}]}
        }
    }}}}
    ---
    {"$id": "user.json", "type": "object", "properties": {
        "__type__": {"type": "string", "enum": ["user"]},
        "name": {"type": "string"}
    }}
"""

import inspect
import logging
import warnings
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, final

from odoo import api, models  # type: ignore[import-untyped]

from ._context import Context
from .exception import InternalError
from .validate import Validation, Validator

logger = logging.getLogger(__name__)


class SkipType:
    def get__type__(self) -> set[str]:
        # Avoid conditions isinstance(converter, SkipType)
        return set()

    @property
    def possible_datatypes(self) -> set[str]:
        # Avoid conditions isinstance(converter, SkipType)
        return set()

    def odoo_datatype(self, instance: models.BaseModel) -> str | None:
        # Avoid conditions isinstance(converter, SkipType)
        return None

    def __bool__(self):
        return False


Skip = SkipType()


class NewinstanceType:
    pass


Newinstance = NewinstanceType()


@final
class Phase:
    @dataclass
    class PreCreate:
        pass

    @dataclass
    class PostCreate:
        pass

    @dataclass
    class Update:
        pass

    @dataclass
    class NamedStage:
        name: str

    Type = PreCreate | PostCreate | Update | NamedStage

    PRECREATE = PreCreate()
    POSTCREATE = PostCreate()
    UPDATE = Update()


class Operation(StrEnum):
    CREATION = "create"
    UPDATE = "update"


class NotAnInstanceGetterException(Exception):
    def __init__(self) -> None:
        super().__init__("Not an instance getter")


class Converter:
    """Base converter class.
    It does not actually convert anything.
    """

    write_stages: Iterable[str] = []

    @property
    def to_odoo_ctx_keys(self) -> Iterable[str]:
        return ()

    @property
    def to_message_ctx_keys(self) -> Iterable[str]:
        return ()

    def __init__(self) -> None:
        self._validation: Validation = Validation.SKIP
        self._validator: None | Validator = None

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        """From an instance, this method returns a matching value for the
        message field.

        :param instance: an instance of an Odoo model
        :param ctx: context built by the caller
        :return: The value or Skip if not included in the message.
        """
        return Skip

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        ctx: Context,
        phase: Phase.Type,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        """From a message, returns a dict.
        Only field whose values are changed are included in the returned dict.

        :param odoo_env: odoo environment
        :param phase: precreate, postcreate, update
        :param message_value: the value of the message
        :param instance: an odoo instance, used to remove existing value from
        the produced dict as needed
        :param value_present: indicate if the value was actually in the message
        (in order to differentiate given None values to non provided values)
        :param ctx: a context built by the caller
        :return: dict of changes to apply on an instance (if any).
        """
        return {}

    @property
    def is_instance_getter(self) -> bool:
        return False

    # XXX should that be moved to a different class, like PostHookConverter
    def get_instance(
        self, odoo_env: api.Environment, ctx: Context, message_data: Any
    ) -> models.BaseModel | NewinstanceType | None:
        """Return an instance of a model. Check is_instance_getter before calling"""
        raise NotAnInstanceGetterException()

    def get__type__(self) -> set[str]:
        """Indicate if this converter is associated to several __type__.
        If so, it will be called with incoming messages associated to them.
        (using message_to_odoo)"""
        return set()

    @property
    def validator(self) -> Validator | None:
        """A validator to use for validation of created messages"""
        return self._get_validator()

    @validator.setter
    def validator(self, value: Validator | None) -> None:
        self._set_validator(value)

    def _get_validator(self) -> Validator | None:
        return self._validator

    def _set_validator(self, value: Validator | None) -> None:
        if value is None:
            self._validator = None
        else:
            if value.initialized:
                self._validator = value
            else:
                raise InternalError(
                    "you must initialize() the validator before passing it"
                )

    @property
    def validation(self) -> Validation:
        return self._get_validation()

    @validation.setter
    def validation(self, value: Validation) -> None:
        self._set_validation(value)

    def _get_validation(self) -> Validation:
        return self._validation

    def _set_validation(self, value: Validation) -> None:
        """Define if validation should be done"""
        assert value is not None
        self._validation = value

    @property
    def possible_datatypes(self) -> set[str]:
        """Possible values for datatype."""
        # A set, as for get___type__, to allow switch to handle different messages.
        return set()

    def odoo_datatype(self, instance: models.BaseModel) -> str | None:
        return None


class PostHookConverter(Converter, metaclass=ABCMeta):
    @abstractmethod
    def post_hook(self, instance: models.BaseModel, message_data):
        """Post hook"""


class Readonly(Converter):
    @property
    def to_odoo_ctx_keys(self) -> Iterable[str]:
        return self._conv.to_odoo_ctx_keys

    @property
    def to_message_ctx_keys(self) -> Iterable[str]:
        return self._conv.to_message_ctx_keys

    def __init__(self, conv: Converter) -> None:
        super().__init__()
        self._conv = conv

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        return self._conv.odoo_to_message(ctx, instance)

    def odoo_datatype(self, instance: models.BaseModel) -> str | None:
        return self._conv.odoo_datatype(instance)


class Writeonly(Converter):
    """A converter that only convert to odoo but does nothing from odoo."""

    @property
    def to_odoo_ctx_keys(self) -> Iterable[str]:
        return self._conv.to_odoo_ctx_keys

    @property
    def to_message_ctx_keys(self) -> Iterable[str]:
        return self._conv.to_message_ctx_keys

    def __init__(self, conv: Converter) -> None:
        super().__init__()
        self._conv = conv

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        ctx: Context,
        phase: Phase.Type,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        return self._conv.message_to_odoo(
            odoo_env, ctx, phase, message_value, instance, value_present
        )

    @property
    def is_instance_getter(self) -> bool:
        return self._conv.is_instance_getter

    def get_instance(
        self, odoo_env: api.Environment, ctx: Context, message_data: Any
    ) -> models.BaseModel | NewinstanceType | None:
        return self._conv.get_instance(odoo_env, ctx, message_data)

    @property
    def possible_datatypes(self) -> set[str]:
        return self._conv.possible_datatypes


class Computed(Converter):
    @staticmethod
    def _to_message_legacy(
        fn: Callable[[models.BaseModel], Any],
    ) -> Callable[[models.BaseModel, Context], Any]:
        def call(instance, _):
            fn(instance)

        return call

    def __init__(
        self,
        to_message: (
            Callable[[models.BaseModel, Context], Any]
            | Callable[[models.BaseModel], Any]
        ),
    ) -> None:
        super().__init__()

        sig = inspect.signature(to_message)
        to_message_arg_count = len(sig.parameters)
        if to_message_arg_count not in (1, 2):
            raise ValueError(
                "Computed 'to_message' callback must have 1 or 2 args:",
                " got {self.to_message_arg_count}",
            )
        if to_message_arg_count == 1:
            warnings.warn(
                "Computed will soon cease to accept 'to_message' callable with "
                "no 'context' argument",
                DeprecationWarning,
                stacklevel=1,
            )
            to_message = self._to_message_legacy(to_message)  # type:ignore[assignment,arg-type]

        self.to_message: Callable[[models.BaseModel, Context], Any] = to_message  # type:ignore[assignment]

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        return self.to_message(instance, ctx)


class Constant(Converter):
    """When building messages, this converter return a constant value."""

    def __init__(self, value: Any) -> None:
        super().__init__()
        self._value = value

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        return self._value


def _create_instance(
    odoo_env: api.Environment,
    ctx: Context,
    converter: Converter,
    message: Any,
    model_name: str,
    extra_changes: Mapping[str, Any] | None = None,
):
    changes = converter.message_to_odoo(
        odoo_env,
        ctx,
        Phase.PRECREATE,
        message,
        None,
    )

    if isinstance(changes, SkipType):
        # Check SkipType instead of Skip for mypy
        changes = {}

    if extra_changes:
        changes.update(extra_changes)

    instance = odoo_env[model_name].create(changes)

    changes = converter.message_to_odoo(
        odoo_env,
        ctx,
        Phase.POSTCREATE,
        message,
        instance,
    )

    if changes:
        instance.write(changes)

    return instance


def _update_instance(
    odoo_env: api.Environment,
    ctx: Context,
    converter: Converter,
    message: Any,
    instance: models.BaseModel,
):
    changes = converter.message_to_odoo(
        odoo_env,
        ctx,
        Phase.UPDATE,
        message,
        instance,
    )

    if changes:
        instance.write(changes)


def _write_stages(
    odoo_env: api.Environment,
    ctx: Context,
    converter: Converter,
    message: Any,
    instance: models.BaseModel,
):
    for stage in converter.write_stages:
        changes = converter.message_to_odoo(
            odoo_env,
            ctx,
            Phase.NamedStage(stage),
            message,
            instance,
        )

        if changes:
            instance.write(changes)


def message_to_odoo(
    odoo_env: api.Environment,
    payload: Mapping,
    model_name: str,
    converter: Converter,
    operation: Operation | None = None,
) -> models.BaseModel:
    """

    :param odoo_env: an Odoo environment
    :param payload: received data
    :param model_name: name of an Odoo model
    :param converter:
    :param operation: if operation is not given, creation will be done if no
       instance can be found by using
       :py:meth:odoo.addons.Converter.get_instance
    :return:
    """
    ctx: Context = {}
    instance: NewinstanceType | models.BaseModel

    if operation == Operation.CREATION:
        instance = Newinstance
    else:
        instance = converter.get_instance(odoo_env, ctx, payload)

    if operation == Operation.CREATION or (
        operation is None and not instance or instance is Newinstance
    ):
        instance = _create_instance(odoo_env, ctx, converter, payload, model_name)

    if operation == Operation.UPDATE or not (
        operation is None and not instance or instance is Newinstance
    ):
        _update_instance(odoo_env, ctx, converter, payload, instance)

    _write_stages(odoo_env, ctx, converter, payload, instance)

    if hasattr(converter, "post_hook"):
        converter.post_hook(instance, payload)

    return instance
