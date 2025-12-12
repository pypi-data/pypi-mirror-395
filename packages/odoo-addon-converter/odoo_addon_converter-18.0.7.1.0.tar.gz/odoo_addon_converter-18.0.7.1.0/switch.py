##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020, 2024, 2025 XCG SAS <https://orbeet.io/>
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
from collections.abc import Callable
from typing import Any

from odoo import api, models  # type: ignore[import-untyped]

from ._context import Context, ContextBuilder
from .base import (
    Converter,
    NewinstanceType,
    Phase,
    PostHookConverter,
    Skip,
    SkipType,
)
from .validate import Validation, Validator


class Switch(PostHookConverter):
    """A converter to handle switch cases.
    A list of converters are provided with a function. The first function to
    match is used, any function that is None will be used.
    The function argument is the model instance.

    Example usage:

    .. code-block:: python

        Switch(
            [
              (
                  lambda record: record.is_xxx,
                  lambda message_value: "wave_code" in message_value,
                  Model("__wave__", {}),
              ),
              (None, None, Model("__event__", {})),
            ]
        )
    """

    def __init__(
        self,
        converters: list[
            tuple[
                Callable[[models.BaseModel], bool] | None,
                Callable[[Any], bool] | None,
                Converter | SkipType,
            ]
        ],
        validator: Validator | None = None,
        validation: Validation = Validation.SKIP,
        context: ContextBuilder | None = None,
    ):
        """
        :param converters: is a 3 tuple composed of:
        out condition, in condition, and chosen converter
        :param validator:
        :param context:
        """
        super().__init__()
        self._converters = converters
        self.context = context
        self.validator = validator
        self.validation = validation

    def odoo_to_message(self, ctx: Context, instance: models.Model) -> Any:
        for out_cond, _in_cond, converter in self._converters:
            if out_cond is None or out_cond(instance):
                if isinstance(converter, SkipType):
                    return converter
                return converter.odoo_to_message(ctx, instance)

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
        for _out_cond, in_cond, converter in self._converters:
            if not isinstance(converter, SkipType) and (
                in_cond is None or in_cond(message_value)
            ):
                return converter.message_to_odoo(
                    odoo_env,
                    ctx,
                    phase,
                    message_value,
                    instance,
                    value_present=value_present,
                )

        return Skip

    @property
    def is_instance_getter(self) -> bool:
        for _out_cond, _in_cond, converter in self._converters:
            if not isinstance(converter, SkipType) and converter.is_instance_getter:
                return True

        return False

    def get_instance(
        self, odoo_env: api.Environment, ctx: Context, message_data: Any
    ) -> models.BaseModel | NewinstanceType | None:
        for _out_cond, in_cond, converter in self._converters:
            if (
                not isinstance(converter, SkipType)
                and converter.is_instance_getter
                and (in_cond is None or in_cond(message_data))
            ):
                return converter.get_instance(odoo_env, ctx, message_data)
        return super().get_instance(odoo_env, ctx, message_data)

    def _set_validator(self, value: Validator | None) -> None:
        # Disabling missing return with super use as this does not return
        # anything other than None.
        # pylint: disable=missing-return
        # also set validator on any converters in our switch, in case they care
        super()._set_validator(value)
        for _out_cond, _in_cond, converter in self._converters:
            if not isinstance(converter, SkipType):
                converter.validator = value

    def _set_validation(self, value: Validation) -> None:
        # Disabling missing return with super use as this does not return
        # anything other than None.
        # pylint: disable=missing-return
        # also set validation on any converters in our switch
        super()._set_validation(value)
        for _out_cond, _in_cond, converter in self._converters:
            if not isinstance(converter, SkipType):
                converter.validation = value

    def get__type__(self) -> set[str]:
        types = set()
        for _out_cond, _in_cond, converter in self._converters:
            types.update(converter.get__type__())
        return types

    @property
    def possible_datatypes(self) -> set[str]:
        result = super().possible_datatypes
        for _out_cond, _in_cond, converter in self._converters:
            result.update(converter.possible_datatypes)
        return result

    def odoo_datatype(self, instance: models.BaseModel) -> str | None:
        for out_cond, _in_cond, converter in self._converters:
            if out_cond is None or out_cond(instance):
                return converter.odoo_datatype(instance)
        return super().odoo_datatype(instance)

    def post_hook(self, instance: models.BaseModel, message_data):
        for _out_cond, in_cond, converter in self._converters:
            if in_cond is None or in_cond(message_data):
                if hasattr(converter, "post_hook"):
                    converter.post_hook(instance, message_data)
                return
