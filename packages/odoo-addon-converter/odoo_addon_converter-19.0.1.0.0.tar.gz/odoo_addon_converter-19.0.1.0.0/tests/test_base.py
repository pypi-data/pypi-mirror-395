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
import typing

from .. import Constant, Field, Model, Xref, message_to_odoo, relation
from ._common import ConverterCase

if typing.TYPE_CHECKING:
    from odoo.addons.base.models.res_users import ResUsers


class Test(ConverterCase):
    def setUp(self):
        super().setUp()
        # get an active user
        self.active_user: ResUsers = self.env["res.users"].search(
            [("active", "=", True)], limit=1
        )

    def test_constant(self):
        converter = Constant("a")
        self.assertEqual("a", converter.odoo_to_message({}, self.env["res.users"]))

    def test_unset_field(self):
        # this tests when a relational substitution
        # is substituted on a record that has not
        # the relation set

        self.assertTrue(self.active_user.create_uid)
        # set its create_uid to False
        self.active_user.write(
            {
                "create_uid": False,
            }
        )

        with self.assertRaises(ValueError) as e:
            relation(
                "create_uid",
                Field("name"),
            )

        self.assertEqual(
            str(e.exception),
            "The model name must be given if the converter should return empty values.",
        )

        converter = Model(
            {
                "user_creator_name": relation(
                    "create_uid(res.users)",
                    Field("name"),
                ),
            },
        )
        message = converter.odoo_to_message({}, self.active_user)
        self.assertEqual(message, {"user_creator_name": ""})

    def test_convert(self):
        converter = Model(
            {
                "active": Field("active"),
                "ref": Xref("base"),
                "name": Field("name"),
                "bic": Field("bic"),
            },
        )
        model_name = "res.bank"
        self.assertTrue(self.env.ref("base.bank_bnp").active)
        message_to_odoo(
            self.env,
            {"ref": "bank_bnp", "active": False},
            model_name,
            converter,
        )
        self.assertFalse(self.env.ref("base.bank_bnp").active)

        message_to_odoo(
            self.env,
            {
                "ref": "bank_new",
                "active": True,
                "name": "New Bank",
                "bic": "CBSBLT26",
            },
            model_name,
            converter,
        )
