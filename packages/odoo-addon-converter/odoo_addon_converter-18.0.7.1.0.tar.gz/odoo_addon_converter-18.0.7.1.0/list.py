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

from typing import Any

from odoo import api, models  # type: ignore[import-untyped]

from ._context import Context, ContextBuilder
from .base import Converter, Phase, SkipType


class List(Converter):
    """A converter that takes a list of converter"""

    def __init__(
        self,
        converters: list[Converter],
        context: ContextBuilder | None = None,
    ):
        super().__init__()
        self._converters = converters
        self.context = context

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        if self.context:
            ctx = self.context._build(ctx, instance, None)

        message_data = []

        for converter in self._converters:
            value = converter.odoo_to_message(ctx, instance)
            if not isinstance(value, SkipType):
                message_data.append(value)

        return message_data

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        ctx: Context,
        phase: Phase.Type,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        result = {}
        for i, converter in enumerate(self._converters):
            new_values = converter.message_to_odoo(
                odoo_env, ctx, phase, message_value[i], instance, value_present
            )
            if not isinstance(new_values, SkipType):
                result.update(new_values)
        return result
