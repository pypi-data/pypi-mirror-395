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
from odoo import tests  # type: ignore[import-untyped]

from .. import (
    Field,
    Model,
    RelationToMany,
    Xref,
    message_to_odoo,
)


class Test(tests.TransactionCase):
    def test_write_stages(self):
        """Write stages is a mechanism to define the order
        in which write operation of sub objects are performed.
        """
        message = {
            "name": "Doe",
            "users": [
                {
                    "login": "johndoe",
                    "company_id": "base.main_company",
                },
            ],
        }
        converter = Model(
            {
                "name": Field("name"),
                "users": Model.annotate(
                    write_stage="user",
                )(
                    RelationToMany(
                        "user_ids",
                        "res.users",
                        Model(
                            {
                                "login": Field("login"),
                                "company_id": Xref(),
                            }
                        ),
                    ),
                ),
            },
            write_stages=["user"],
        )
        partner = message_to_odoo(
            self.env,
            message,
            "res.partner",
            converter,
        )
        self.assertTrue(partner)
        self.assertEqual(partner.name, "Doe")
        self.assertTrue(partner.user_ids)
        self.assertEqual(partner.user_ids[0].login, "johndoe")
