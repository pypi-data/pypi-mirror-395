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
from collections.abc import Callable
from typing import Any

from odoo import api, models  # type: ignore[import-untyped]

from . import base
from ._context import Context, ContextBuilder, build_context
from .base import (
    Converter,
    NewinstanceType,
    Phase,
    Skip,
    SkipType,
)
from .field import Field

_logger = logging.getLogger(__name__)


class _RelationBase(Field):
    def __init__(
        self,
        field_name: str,
        model_name: str,
        converter: Converter,
        to_message_context: ContextBuilder,
        to_odoo_context: ContextBuilder,
    ):
        super().__init__(field_name)
        self.converter = converter
        self.model_name = model_name
        self._to_message_context = to_message_context
        self._to_odoo_context = to_odoo_context

        self._to_odoo_context.inherit_if_missing(self.converter.to_odoo_ctx_keys)

    @property
    def to_odoo_ctx_keys(self):
        return self._to_odoo_context.inherited()


class RelationToOne(_RelationBase):
    def __init__(
        self,
        field_name: str,
        model_name: str | None,
        converter: Converter,
        send_empty: bool = True,
        to_message_context: ContextBuilder | None = None,
        to_odoo_context: ContextBuilder | None = None,
    ):
        super().__init__(
            field_name,
            model_name or "",
            converter,
            to_message_context or ContextBuilder(),
            to_odoo_context or ContextBuilder(),
        )
        self._send_empty = send_empty
        if send_empty and not model_name:
            raise ValueError(
                "The model name must be given if the converter should return "
                "empty values."
            )

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        ctx = build_context(
            self._to_message_context,
            ctx,
            instance,
            None,
        )
        # do not use super, otherwise if empty, will convert that
        relation_instance = getattr(instance, self.field_name)
        if not relation_instance:
            if not self._send_empty:
                return Skip
            relation_instance = instance.env[self.model_name]
        return self.converter.odoo_to_message(ctx, relation_instance)

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        ctx: Context,
        phase: Phase.Type,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        if not value_present:
            return {}

        ctx = build_context(
            self._to_odoo_context,
            ctx,
            instance,
            message_value,
        )

        record = _update_record(
            self, odoo_env, ctx, phase, message_value, instance, value_present
        )
        if record is None:
            return {}

        if instance and not isinstance(instance, NewinstanceType):
            field_value = getattr(instance, self.field_name)
            if field_value and record.id in field_value.ids:
                return {}

        return {self.field_name: record.id}


class RelationToMany(_RelationBase):
    def __init__(
        self,
        field_name: str,
        model_name: str | None,
        converter: Converter,
        sortkey: None | Callable[[models.BaseModel], bool] = None,
        filtered: None | str | Callable[[models.BaseModel], bool] = None,
        to_message_context: ContextBuilder | None = None,
        to_odoo_context: ContextBuilder | None = None,
        limit: Any | None = None,
        readonly: bool = False,
    ):
        """
        :param filtered: filter to use in Odoo’s BaseModel filtered method.
        """
        if not readonly and not converter.is_instance_getter:
            raise ValueError(
                "On non-readonly RelationToMany, converter must be an instance getter"
            )
        super().__init__(
            field_name,
            model_name or "",
            converter,
            to_message_context or ContextBuilder(),
            to_odoo_context or ContextBuilder(),
        )
        self.filtered = filtered
        self.sortkey = sortkey
        self.limit = limit

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        ctx = build_context(
            self._to_message_context,
            ctx,
            instance,
            None,
        )

        value = super().odoo_to_message(ctx, instance)
        if isinstance(value, SkipType):
            return value
        if self.filtered:
            value = value.filtered(self.filtered)
        if self.sortkey:
            value = value.sorted(key=self.sortkey)
        if self.limit:
            value = value[: self.limit]

        return [
            m
            for m in (self.converter.odoo_to_message(ctx, r) for r in value)
            if not isinstance(m, SkipType)
        ]

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        ctx: Context,
        phase: Phase.Type,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        # if not present or value is None, do not update the values.
        if not value_present or message_value is None:
            return {}

        ctx = build_context(
            self._to_odoo_context,
            ctx,
            instance,
            message_value,
        )

        field_instances = odoo_env[self.model_name]
        for value in message_value:
            record = _update_record(
                self, odoo_env, ctx, phase, value, instance, value_present
            )
            if record is not None:
                field_instances |= record

        if (
            instance
            and not isinstance(instance, NewinstanceType)
            and getattr(instance, self.field_name) == field_instances
        ):
            return {}
        return {self.field_name: [(6, 0, field_instances.ids)]}


class RelationToManyMap(Field):
    def __init__(
        self,
        field_name: str,
        model_name: str | None,
        key_converter: Converter,
        value_converter: Converter,
        filtered: None | str | Callable[[models.BaseModel], bool] = None,
        to_message_context: ContextBuilder | None = None,
        to_odoo_context: ContextBuilder | None = None,
        readonly: bool = False,
    ):
        """
        :param filtered: filter to use in Odoo’s BaseModel filtered method.
        """
        if not readonly and not (
            key_converter.is_instance_getter or value_converter.is_instance_getter
        ):
            raise ValueError(
                "On non-readonly RelationToManyMap, converter must be an "
                "instance getter"
            )
        super().__init__(field_name)
        self.key_converter = key_converter
        self.value_converter = value_converter
        self.model_name = model_name
        self.filtered = filtered
        self._to_message_context = to_message_context
        self._to_odoo_context = to_odoo_context

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        ctx = build_context(
            self._to_message_context,
            ctx,
            instance,
            None,
        )

        value = super().odoo_to_message(ctx, instance)
        if isinstance(value, SkipType):
            return value
        if self.filtered:
            value = value.filtered(self.filtered)
        return {
            k: v
            for k, v in (
                (
                    self.key_converter.odoo_to_message(ctx, r),
                    self.value_converter.odoo_to_message(ctx, r),
                )
                for r in value
            )
            if not isinstance(k, SkipType) and not isinstance(v, SkipType)
        }

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        ctx: Context,
        phase: Phase.Type,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        # TODO _update_record requires a 'converter' attribute on 'self',
        # which RelationToManyMap does not have. This function is thereby
        # doomed to crash.

        # if not present or value is None, do not update the values.
        if not value_present or message_value is None:
            return {}
        ctx = build_context(
            self._to_odoo_context,
            ctx,
            instance,
            message_value,
        )
        field_instances = odoo_env[self.model_name]
        for value in message_value:
            record = _update_record(
                self, odoo_env, ctx, phase, value, instance, value_present
            )
            if record is not None:
                field_instances |= record

        if (
            instance
            and not isinstance(instance, NewinstanceType)
            and getattr(instance, self.field_name) == field_instances
        ):
            return {}
        return {self.field_name: [(6, 0, field_instances.ids)]}


def relation(path: str, converter: Converter) -> Converter:
    """Note: Can return RelationToOne with an x2m field if path
    does not contain '[]'.
    """
    for name in reversed(path.split("/")):
        model_name = None
        pi = name.find("(")
        if pi != -1:
            if not name.endswith(")"):
                raise ValueError(f"Invalid path: {name}")
            model_name = name[pi + 1 : -1]  # noqa: E203
            name = name[:pi]
        if name.endswith("[]"):
            converter = RelationToMany(name[:-2], model_name, converter)
        else:
            converter = RelationToOne(name, model_name, converter)
    return converter


def _update_record(
    self,
    odoo_env: api.Environment,
    ctx: Context,
    phase: Phase.Type,
    message_value: Any,
    instance: models.BaseModel,
    value_present: bool = True,
) -> Any:
    """Update or create a single record with the given values.
    :param self: the actual converter class.
    :param message_value: the message value for one record.
    :return: the record id, if any, else None.
    """
    post_hook = getattr(self.converter, "post_hook", None)

    if self.converter.is_instance_getter:
        rel_record: models.BaseModel | NewinstanceType | None = (
            self.converter.get_instance(odoo_env, ctx, message_value)
        )
        if rel_record is None:
            return None

        if isinstance(rel_record, NewinstanceType):
            rel_record = None

        if rel_record is None:
            extra_changes = None
            if instance:
                field = instance._fields[self.field_name]
                if field.type == "one2many":
                    extra_changes = {field.inverse_name: instance.id}

            rel_record = base._create_instance(
                odoo_env,
                ctx,
                self.converter,
                message_value,
                self.model_name,
                extra_changes=extra_changes,
            )
        else:
            base._update_instance(
                odoo_env, ctx, self.converter, message_value, rel_record
            )

        base._write_stages(odoo_env, ctx, self.converter, message_value, rel_record)

        if post_hook:
            post_hook(rel_record, message_value)

        return rel_record

    field_value = (
        getattr(instance, self.field_name)
        if instance and not isinstance(instance, NewinstanceType)
        else None
    )

    updates = self.converter.message_to_odoo(
        odoo_env, ctx, phase, message_value, field_value, value_present
    )

    if updates:
        if field_value:
            field_value.write(updates)
            if post_hook:
                post_hook(field_value, message_value)
            return None
        rel_record = odoo_env[self.model_name].create(updates)
        if post_hook:
            post_hook(rel_record, message_value)
        return rel_record
    return None
