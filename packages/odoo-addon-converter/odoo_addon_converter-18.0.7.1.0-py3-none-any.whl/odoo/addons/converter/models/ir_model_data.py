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

import uuid
from typing import Final

from odoo import api, models  # type: ignore[import-untyped]

# Xrefs are stored within "ir.model.data" with this module name.
_XREF_IMD_MODULE: Final[str] = "__converter__"


class IrModelData(models.BaseModel):
    """Add xref tools.
    All done with the super-admin user to bypass security rules.

    xrefs are stored within "ir.model.data" with a special module name.
    xrefs are always UUIDs.
    """

    _inherit = "ir.model.data"

    @api.model
    def generate_name(self, prefix: str = "") -> str:
        """Generate an xref for odoo record;
        :param prefix: prefix to use before the name.
        :return: a UUID from a string of 32 hex digit
        """

        return prefix + uuid.uuid4().hex

    @api.model
    def object_to_module_and_name(
        self,
        record_set: models.BaseModel,
        module: str | None = _XREF_IMD_MODULE,
        prefix: str = "",
    ) -> tuple[str, str]:
        """Retrieve an xref pointing to the specified Odoo record; create one
        when missing.
        :param module: Name of the module to use. None to use any name, if no
        xmlid exists "" will be used as the module name.
        :param prefix: prefix to use before the name.
        :return: tuple module and name
        """
        record_set.ensure_one()

        domain = [
            ("res_id", "=", record_set.id),
            ("model", "=", record_set._name),
        ]
        if module is not None:
            domain.append(("module", "=", module))
        if prefix:
            domain.append(("name", "=like", f"{prefix}%"))

        # Find an existing xref. See class docstring for details.
        imd = self.sudo().search(domain, limit=1)
        if imd:
            return imd.module, imd.name

        # Could not find an existing xref; create one.
        name = self.generate_name(prefix)
        if module is None:
            module = ""
        self.set_xmlid(record_set, name, module)
        return module, name

    @api.model
    def object_to_xmlid(
        self,
        record_set: models.BaseModel,
        module: str | None = _XREF_IMD_MODULE,
        prefix: str = "",
    ) -> str:
        """Retrieve an xref pointing to the specified Odoo record; create one
        when missing.
        :param module: Name of the module to use. None to use any name, if no
        xmlid exists "" will be used as the module name.
        :param prefix: prefix to use before the name.
        """
        return "{0[0]}.{0[1]}".format(
            self.object_to_module_and_name(record_set, module, prefix)
        )

    @api.model
    def set_xmlid(
        self,
        record_set: models.BaseModel,
        name: str,
        module: str = _XREF_IMD_MODULE,
        only_when_missing: bool = False,
    ):
        """Save an external reference to the specified Odoo record.
        :param module: Name of the module to use.
        :param only_when_missing: Check before creating a duplicate.
        """
        record_set.ensure_one()

        if only_when_missing and self.sudo().search(
            [
                ("res_id", "=", record_set.id),
                ("model", "=", record_set._name),
                ("module", "=", module),
            ],
            limit=1,
        ):
            return

        self.sudo().create(
            {
                "name": name,
                "model": record_set._name,
                "module": module,
                "res_id": record_set.id,
            }
        )
