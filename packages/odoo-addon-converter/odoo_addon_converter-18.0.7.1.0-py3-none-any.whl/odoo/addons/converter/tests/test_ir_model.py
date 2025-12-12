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

from odoo.tests import TransactionCase, tagged  # type: ignore[import-untyped]


@tagged("post_install", "-at_install")
class Test(TransactionCase):
    def test_get_xmlid_present(self):
        """Ensure we get a new UUID-ish xref when a record already has an
        external ID.
        """

        view_menu = self.browse_ref("base.edit_menu_access")
        module, xref = self.env["ir.model.data"].object_to_module_and_name(view_menu)
        self.assertTrue(xref)
        self.assertNotIn(".", xref)
        self.assertNotEqual(xref, "view_menu")

        # Also check the standard ir.model.data method here.
        self.assertEqual(
            self.ref(f"{module}.{xref}"),
            view_menu.id,
        )

    def test_get_xmlid_absent(self):
        obj = self.env["ir.config_parameter"].create({"key": "something", "value": 1})
        module, xref = self.env["ir.model.data"].object_to_module_and_name(obj)
        self.assertTrue(xref)
        self.assertNotIn(".", xref)

        # Also check the standard ir.model.data method here.
        new_recset = self.browse_ref(f"{module}.{xref}")
        self.assertEqual(new_recset.id, obj.id)
