##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020, 2024 XCG SAS <https://orbeet.io/>
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
import logging
import traceback
from collections import OrderedDict
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Final

from odoo import api, models
from odoo.exceptions import UserError

from ._context import Context, ContextBuilder, build_context
from .base import (
    Converter,
    Newinstance,
    NewinstanceType,
    Phase,
    PostHookConverter,
    SkipType,
)
from .validate import NotInitialized, Validation, Validator

try:
    from fastjsonschema import JsonSchemaException  # type: ignore[import-untyped]
except ImportError:
    # Ignore no-redef, added for compatibility
    class JsonSchemaException(Exception):  # type: ignore[no-redef]
        """Custom error in case of missing optional requirement"""


_logger = logging.getLogger(__name__)


class IncorrectTypeException(Exception):
    """__type__ is in the message is not the same as the expected value"""


class MissingRequiredValidatorException(Exception):
    def __init__(self):
        super().__init__("Strict validation without validator")


class Model(PostHookConverter):  # pylint: disable=too-many-instance-attributes
    """A converter that takes a dict of key, used when a message has values"""

    @property
    def to_odoo_ctx_keys(self):
        if self._to_odoo_context is None:
            return ()

        return self._to_odoo_context.inherited()

    @dataclass
    class AnnotatedConverter(Converter):
        converter: Converter
        write_stage: str | None = None
        to_odoo_context: ContextBuilder | None = None
        to_message_context: ContextBuilder | None = None

        def ensure_to_odoo_context(self) -> ContextBuilder:
            if self.to_odoo_context is None:
                self.to_odoo_context = ContextBuilder()

            return self.to_odoo_context

        def ensure_to_message_context(self) -> ContextBuilder:
            if self.to_message_context is None:
                self.to_message_context = ContextBuilder()

            return self.to_message_context

        def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
            return self.converter.odoo_to_message(ctx, instance)

        def odoo_datatype(self, instance: models.BaseModel) -> str | None:
            return self.converter.odoo_datatype(instance)

        def message_to_odoo(
            self,
            odoo_env: api.Environment,
            ctx: Context,
            phase: Phase.Type,
            message_value: Any,
            instance: models.BaseModel,
            value_present: bool = True,
        ) -> dict | SkipType:
            return self.converter.message_to_odoo(
                odoo_env, ctx, phase, message_value, instance, value_present
            )

        @property
        def is_instance_getter(self) -> bool:
            return self.converter.is_instance_getter

        def get_instance(
            self, odoo_env: api.Environment, ctx: Context, message_data: Any
        ) -> models.BaseModel | NewinstanceType | None:
            return self.converter.get_instance(odoo_env, ctx, message_data)

        @property
        def possible_datatypes(self) -> set[str]:
            return self.converter.possible_datatypes

    @staticmethod
    def annotate(
        write_stage: str | None = None,
        to_odoo_context: ContextBuilder | None = None,
        to_message_context: ContextBuilder | None = None,
    ) -> Callable[[Converter], AnnotatedConverter]:
        return lambda converter: Model.AnnotatedConverter(
            converter=converter,
            write_stage=write_stage,
            to_odoo_context=to_odoo_context,
            to_message_context=to_message_context,
        )

    # Disabling pylint on number of arguments. Do not add more.
    def __init__(  # pylint: disable=too-many-positional-arguments,too-many-arguments
        self,
        converters: Mapping[str, AnnotatedConverter | Converter],
        json_schema: str | None = None,
        # The validator is usually not given at this point but is common
        # throughout a project. That’s why it is a property
        validator: Validator | None = None,
        merge_with: Iterable[Converter] | None = None,
        validation: Validation = Validation.SKIP,
        to_message_context: ContextBuilder | None = None,
        to_odoo_context: ContextBuilder | None = None,
        datatype: str | None = None,
        __type__: str | None = None,
        write_stages: Iterable[str] = (),
    ):
        """
        :param datatype: datatype to use. Usually used with None __type__.
        """
        super().__init__()
        self._type: str | None = __type__
        self._post_hooks_converters: dict[str, PostHookConverter] = {}
        self._jsonschema: str | None = json_schema
        self._get_instance: str | None = None
        """First converter whose `is_instance_getter` is true if any"""
        self.merge_with: Iterable[Converter] | None = merge_with
        self._to_message_context = to_message_context
        self._to_odoo_context = to_odoo_context
        self.validator = validator
        self.validation = validation
        self._datatype: Final[str | None] = datatype
        self.write_stages = write_stages

        converters_dict = {}
        for key, converter in converters.items():
            if self._get_instance is None and converter.is_instance_getter:
                self._get_instance = key

            if isinstance(converter, PostHookConverter):
                self._post_hooks_converters[key] = converter

            # A converter that needs context keys has to be annotated to a
            # context builder is associated to it
            if (
                not isinstance(converter, Model.AnnotatedConverter)
                and converter.to_odoo_ctx_keys
            ):
                converter = Model.AnnotatedConverter(converter)

            if isinstance(converter, Model.AnnotatedConverter):
                child_context = converter.ensure_to_odoo_context()
                child_context.inherit_if_missing(converter.converter.to_odoo_ctx_keys)
                self.ensure_to_odoo_context().inherit_if_missing(
                    child_context.inherited()
                )

            converters_dict[key] = converter

        self._converters: Mapping[str, Model.AnnotatedConverter | Converter] = (
            converters_dict
        )

    def ensure_to_odoo_context(self):
        if self._to_odoo_context is None:
            self._to_odoo_context = ContextBuilder()
        return self._to_odoo_context

    @staticmethod
    def _build_context(
        converter: AnnotatedConverter | Converter,
        to_odoo: bool,
        ctx: Context,
        instance,
        message,
    ):
        if isinstance(converter, Model.AnnotatedConverter):
            if to_odoo:
                if converter.to_odoo_context:
                    return build_context(
                        converter.to_odoo_context,
                        ctx,
                        instance,
                        message,
                    )
            else:
                if converter.to_message_context:
                    return build_context(
                        converter.to_message_context,
                        ctx,
                        instance,
                        message,
                    )
        return {}

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        ctx = build_context(self._to_message_context, ctx, instance, None)

        message_data = {}
        if self._type is not None:
            message_data["__type__"] = self._type

        errors = []
        for key, converter in self._converters.items():
            cctx = Model._build_context(converter, False, ctx, instance, None)
            try:
                value = converter.odoo_to_message(cctx, instance)
            except Exception as e:  # pylint: disable=broad-exception-caught
                errors.append(
                    {"key": key, "traceback": "".join(traceback.format_exception(e))}
                )
                continue
            if not isinstance(value, SkipType):
                message_data[key] = value
        if len(errors) != 0:
            formatted_errors = "\n\n".join(
                [f"{error['traceback']}Key: {error['key']}" for error in errors]
            )
            raise UserError(
                instance._(
                    "Got unexpected errors while parsing substitutions:\n%s",
                    formatted_errors,
                )
            )

        # XXX we could rebuild the context with message_data as the 'message'
        # This would allow adding values from the message built by the first
        # converters to the context passed to the 'merge_with' converters

        if self.merge_with:
            for conv in self.merge_with:
                value = conv.odoo_to_message(ctx, instance)
                if isinstance(value, SkipType):
                    continue
                message_data.update(value)

        if self.validation != Validation.SKIP and self._jsonschema is not None:
            if self.validator:
                try:
                    self.validator.validate(self._jsonschema, message_data)
                except (NotInitialized, JsonSchemaException):
                    _logger.warning("Validation failed", exc_info=True)
                    if self.validation == Validation.STRICT:
                        raise
            elif self.validation == Validation.STRICT:
                raise MissingRequiredValidatorException()

        return message_data

    @staticmethod
    def _skip_phase(converter: AnnotatedConverter | Converter, phase: Phase.Type):
        """Returns wether a converter should be skipped at a given phase based
        on its 'write_stage' annotation (which defaults to None)"""

        write_stage = None

        if isinstance(converter, Model.AnnotatedConverter):
            write_stage = converter.write_stage

        match phase:
            case Phase.NamedStage(name):
                return name != write_stage

            case _:
                return write_stage is not None

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        ctx: Context,
        phase: Phase.Type,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        ctx = build_context(self._to_odoo_context, ctx, instance, message_value)

        values: dict[str, Any] = OrderedDict()

        if self.validation != Validation.SKIP and self._jsonschema is not None:
            if self.validator:
                try:
                    self.validator.validate(self._jsonschema, message_value)
                except (NotInitialized, JsonSchemaException):
                    _logger.warning("Validation failed", exc_info=True)
                    if self.validation == Validation.STRICT:
                        raise
            elif self.validation == Validation.STRICT:
                raise MissingRequiredValidatorException()

        if self._type is not None and message_value["__type__"] != self._type:
            raise IncorrectTypeException(
                "Expected __type__ {}, found {}".format(
                    self._type, message_value["__type__"]
                )
            )
        for key, converter in self._converters.items():
            if Model._skip_phase(converter, phase):
                continue

            cctx = Model._build_context(converter, True, ctx, instance, message_value)
            value = message_value.get(key, None) if message_value else None
            attribute_vals = converter.message_to_odoo(
                odoo_env,
                cctx,
                phase,
                value,
                instance,
                message_value and key in message_value,
            )
            # cannot use 'is Skip' because of mypy
            if isinstance(attribute_vals, SkipType):
                continue

            values.update(attribute_vals)
        if self.merge_with:
            for conv in self.merge_with:
                value = conv.message_to_odoo(
                    odoo_env,
                    ctx,
                    phase,
                    message_value,
                    instance,
                    value_present,
                )
                if isinstance(value, SkipType):
                    continue
                values.update(value)

        return values

    @property
    def is_instance_getter(self) -> bool:
        return self._get_instance is not None

    def get_instance(
        self, odoo_env: api.Environment, ctx: Context, message_data: Any
    ) -> models.BaseModel | NewinstanceType | None:
        """:return: an instance linked to the converter, if any"""

        ctx = build_context(self._to_odoo_context, ctx, None, message_data)

        if self._get_instance:
            instance = self._converters[self._get_instance].get_instance(
                odoo_env, ctx, message_data[self._get_instance]
            )
            if instance is None:
                instance = Newinstance
            return instance
        return None

    def post_hook(self, instance: models.BaseModel, message_data):
        for key in self._post_hooks_converters:
            if key in message_data:
                self._post_hooks_converters[key].post_hook(instance, message_data[key])
        if self.merge_with:
            for converter in self.merge_with:
                if hasattr(converter, "post_hook"):
                    converter.post_hook(instance, message_data)

    def get__type__(self) -> set[str]:
        return set() if self._type is None else {self._type}

    @property
    def possible_datatypes(self) -> set[str]:
        result = set()
        if self._datatype is not None:
            result.add(self._datatype)
        return result

    def odoo_datatype(self, instance: models.BaseModel) -> str | None:
        return self._datatype
