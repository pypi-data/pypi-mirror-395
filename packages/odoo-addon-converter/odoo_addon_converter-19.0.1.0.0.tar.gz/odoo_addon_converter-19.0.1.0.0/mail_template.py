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
import ast
from typing import Any

from odoo import models  # type: ignore[import-untyped]

from .base import Context, Converter


class MailTemplate(Converter):
    """This converter wraps ``mail.template::_render_template``.
    Multiple records are allowed but ``mail.template::_render_template`` still
    runs once per record; to accommodate, we provide ``ctx["records"]``.

    Using this converter requires the mail module to be installed.
    """

    def __init__(self, template: str, post_eval: bool = False):
        super().__init__()
        self.template = template
        self.post_eval = post_eval

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        value = (
            instance.env["mail.template"]
            .with_context(records=instance, safe=True)
            ._render_template(self.template, instance._name, instance.ids)
        )
        value = value[instance[0].id]  # _render_template outputs indexed by record ID
        if self.post_eval:
            value = ast.literal_eval(value)
        return value
