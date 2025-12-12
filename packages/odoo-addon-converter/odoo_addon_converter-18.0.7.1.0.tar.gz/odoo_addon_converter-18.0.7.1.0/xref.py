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
import logging
import os
import uuid
from typing import Any, Final

from odoo import _, api, models  # type: ignore[import-untyped]

from ._context import Context, ContextBuilder
from .base import Converter, NewinstanceType, PostHookConverter
from .models.ir_model_data import _XREF_IMD_MODULE

_logger = logging.getLogger(__name__)


# TODO dans quel cas ça ne pourrait pas être un instance getter???
class Xref(PostHookConverter):
    """This converter represents an external reference, using the standard xmlid with a
    custom module name.
    """

    def __init__(
        self,
        module: str | None = _XREF_IMD_MODULE,
        is_instance_getter: bool = True,
        include_module_name: bool = False,
        prefix: str = "",
    ):
        """
        :param prefix: prefix to use in ir.model.data, nor sent nor received.
          Used to prevent duplication if received id is too simple.
        """
        super().__init__()
        self._module = module
        self._is_instance_getter = is_instance_getter
        self._include_module_name: Final[bool] = include_module_name
        self._prefix: Final[str] = prefix

    def odoo_to_message(self, ctx: Context, instance: models.Model) -> Any:
        if not instance:
            return ""
        module, name = instance.env["ir.model.data"].object_to_module_and_name(
            instance, self._module, self._prefix
        )
        if self._prefix is not None:
            name = name[len(self._prefix) :]
        if self._include_module_name:
            return f"{module}.{name}"
        return name

    def get_instance(
        self, odoo_env: api.Environment, ctx: Context, message_data: Any
    ) -> models.BaseModel | NewinstanceType | None:
        if self._is_instance_getter:
            module, name = self._module_name(message_data)
            return odoo_env.ref(
                f"{module}.{name}",
                raise_if_not_found=False,
            )
        return None

    def post_hook(self, instance: models.BaseModel, message_data):
        # add xmlid to the newly created object
        module, name = self._module_name(message_data)
        instance.env["ir.model.data"].set_xmlid(
            instance, name, module=module, only_when_missing=True
        )

    def _module_name(self, value: str) -> tuple[str, str]:
        """Return module and name depending on options"""
        module = "" if self._module is None else self._module
        name = value
        if self._include_module_name:
            module, name = value.split(".", 1)
            assert module == self._module
        if self._prefix is not None:
            name = self._prefix + name
        return module, name

    @property
    def is_instance_getter(self) -> bool:
        return self._is_instance_getter


class JsonLD_ID(Xref):
    """This converter represents a JsonLD ID , an url made of
    a base part defined as ir.config_parameter, an optional breadcrumb
    and a unique id part using the standard xmlid.
    """

    def __init__(
        self,
        breadcrumb: str | Converter,
        module: str | None = _XREF_IMD_MODULE,
        is_instance_getter: bool = True,
        unique_id_field: str | None = None,
        context: ContextBuilder | None = None,
        has_base_url: bool = True,
    ):
        """
        :param breadcrumb: Part of the url describing the entity,
        must match the syntax expected by os.path, ie absolute path
        begins with a slash. With absolute path the base part is
        ignored. Can also be a converter, if so, the result of the
        combined converters must be a string.
        """
        super().__init__(
            module=module,
            is_instance_getter=is_instance_getter,
        )
        self.converter: Converter | None = None
        self._breadcrumb = breadcrumb if isinstance(breadcrumb, str) else None
        if isinstance(breadcrumb, Converter):
            self.converter = breadcrumb
        self._unique_id_field = unique_id_field
        self._context = context
        self._has_base_url = has_base_url

    def odoo_to_message(self, ctx: Context, instance: models.Model) -> Any:
        if not instance:
            return ""

        imds = (
            instance.env["ir.model.data"]
            .sudo()
            .search(
                [
                    ("module", "=", self._module),
                    ("model", "=", instance._name),
                    ("res_id", "=", instance.id),
                ]
            )
        )

        if self._context is not None:
            ctx = self._context._build(ctx, instance, None)
        jsonld_id_base_url = (
            instance.env["ir.config_parameter"]
            .sudo()
            .get_param("sync.jsonld_id_base_url")
        )
        if self._has_base_url and not jsonld_id_base_url:
            _logger.error(
                _("Missing config parameter: 'sync.jsonld_id_base_url' is not defined")
            )
            return ""

        if self.converter is not None:
            self._breadcrumb = self.converter.odoo_to_message(instance, ctx)

        # xref does not exist or does not match the jsonld expected format, create it
        schema_base = os.path.join(
            jsonld_id_base_url if self._has_base_url else "",
            self._breadcrumb if self._breadcrumb is not None else "",
        )
        if not imds or all(not imd.name.startswith(schema_base) for imd in imds):
            if self._unique_id_field is not None:
                name = getattr(instance, self._unique_id_field)
            else:
                name = uuid.uuid4().hex

            xref = os.path.join(schema_base, name)
            instance.env["ir.model.data"].set_xmlid(instance, xref, module=self._module)
        else:
            for imd in imds:
                if imd.name.startswith(schema_base):
                    xref = imd.name
        return xref
