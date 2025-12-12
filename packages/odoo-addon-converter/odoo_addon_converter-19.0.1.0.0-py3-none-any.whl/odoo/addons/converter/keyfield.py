##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020 XCG SAS <https://orbeet.io/>
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

from collections.abc import Callable, Iterable, Mapping
from typing import Any

from odoo import api, models  # type: ignore[import-untyped]
from typing_extensions import override

from ._context import Context
from .base import Converter, NewinstanceType, Phase, Skip, SkipType

LookupFilterFactory = Callable[[Context, Mapping], list[tuple[str, str, Any]]]


class KeyField(Converter):
    """Converter used when a field is used as a key.

    This is usually used with a RelationToX converter instead of a
    :class:Xref converter.

    The key must match only one model. Set limit_lookup to use the first model found.
    """

    def __init__(
        self,
        field_name: str,
        model_name: str,
        limit_lookup: bool = False,
        lookup_scope: LookupFilterFactory | None = None,
        to_odoo_ctx_keys: Iterable[str] = (),
    ):
        super().__init__()
        self.field_name = field_name
        self.model_name = model_name
        self.lookup_limit = 1 if limit_lookup else None
        self._lookup_scope = lookup_scope
        self._to_odoo_ctx_keys = to_odoo_ctx_keys

    @override
    @property
    def to_odoo_ctx_keys(self) -> Iterable[str]:
        return self._to_odoo_ctx_keys

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        return getattr(instance, self.field_name)

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
            return Skip

        if instance and getattr(instance, self.field_name) == message_value:
            return Skip

        return {self.field_name: message_value}

    def get_instance(
        self, odoo_env: api.Environment, ctx: Context, message_data: Any
    ) -> models.BaseModel | NewinstanceType | None:
        domain = [(self.field_name, "=", message_data)]
        if self._lookup_scope:
            domain.extend(self._lookup_scope(ctx, message_data))

        instance = odoo_env[self.model_name].search(domain, limit=self.lookup_limit)
        if not instance:
            return None
        instance.ensure_one()
        return instance

    @property
    def is_instance_getter(self) -> bool:
        return True
