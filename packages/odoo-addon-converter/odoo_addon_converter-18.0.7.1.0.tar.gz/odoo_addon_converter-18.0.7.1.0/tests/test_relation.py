##############################################################################
#
#    Converter Odoo module
#    Copyright © 2021, 2024, 2025 XCG SAS <https://orbeet.io/>
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

from odoo import tests  # type: ignore[import-untyped]

from .. import Field, Model, RelationToMany, RelationToOne, Skip, Xref, message_to_odoo


class Test(tests.TransactionCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.converter1 = RelationToOne(
            "company_id", "res.company", Xref(None, prefix="main_")
        )
        cls.converter2 = RelationToOne("action_id", "res.company", Xref(None))
        cls.converter3 = RelationToOne(
            "action_id", "res.company", Xref(None), send_empty=False
        )
        cls.converter4 = RelationToOne(
            "company_id", "res.company", Xref(None), send_empty=False
        )

    def setUp(self):
        super().setUp()
        self.user_root = self.env.ref("base.user_root")
        self.user_admin = self.env.ref("base.user_admin")

    def test_many2one_from_odoo(self):
        message = self.converter1.odoo_to_message({}, self.user_admin)
        self.assertEqual(message, "company")
        message = self.converter1.odoo_to_message({}, self.user_root)
        self.assertEqual(message, "company")

    def test_many2one_skip_from_odoo(self):
        message = self.converter4.odoo_to_message({}, self.user_admin)
        self.assertEqual(message, "main_company")

    def test_empty_many2one_from_odoo(self):
        message = self.converter2.odoo_to_message({}, self.user_root)
        self.assertEqual(message, "")

    def test_empty_many2one_skip_from_odoo(self):
        message = self.converter3.odoo_to_message({}, self.user_root)
        self.assertEqual(message, Skip)

    def test_many2one_to_odoo(self):
        """Ensure a sub-object linked from the main one gets updated when Odoo
        receives a message.
        """

        # This converter wraps a user and adds info from its related partner.
        converter = Model(
            {
                "partner": RelationToOne(
                    "partner_id",
                    "res.partner",
                    Model(
                        {
                            "color": Field("color"),
                            "name": Field("name"),
                            "xref": Xref("test"),
                        },
                        __type__="partner",
                    ),
                ),
                "xref": Xref("base"),
            },
        )

        user = self.env.ref("base.user_admin")
        old_partner = user.partner_id

        # Run our message reception.
        message: dict[str, Any] = {
            "partner": {
                "__type__": "partner",
                "color": 2,
                "name": "TEST",
                "xref": "new_partner_converter",
            },
            "xref": "user_admin",
        }
        message_to_odoo(self.env, message, self.env["res.users"], converter)

        # Ensure a new partner got created and that it has an xref (post hook).
        new_partner = self.env.ref("test.new_partner_converter")
        self.assertEqual(user.partner_id, new_partner)
        self.assertNotEqual(new_partner, old_partner)
        self.assertEqual(new_partner.color, 2)
        self.assertEqual(new_partner.name, "TEST")

        # Try again with the same partner ref; check update (but no creations).
        message["partner"]["color"] = 3
        message_to_odoo(self.env, message, self.env["res.users"], converter)
        self.assertEqual(user.partner_id, new_partner)
        self.assertEqual(new_partner.color, 3)

    def test_many2many_to_odoo(self):
        """Ensure multiple sub-objects linked from the main one gets updated
        when Odoo receives a message.
        """

        # This converter wraps a user and adds info from its related partner.
        converter = Model(
            {
                "users": RelationToMany(
                    "user_ids",
                    "res.users",
                    Model(
                        {
                            "email": Field("email"),
                            "xref": Xref("base"),
                        },
                        __type__="user",
                    ),
                ),
                "xref": Xref("base"),
            },
        )

        partner = self.env.ref("base.main_partner")
        self.assertFalse(partner.user_ids)

        # Run our message reception.
        message: dict[str, Any] = {
            "users": [
                {
                    "__type__": "user",
                    "xref": "user_admin",
                },
                {
                    "__type__": "user",
                    "xref": "user_demo",
                },
            ],
            "xref": "main_partner",
        }
        message_to_odoo(self.env, message, self.env["res.partner"], converter)

        # Check the partner's users
        self.assertTrue(partner.user_ids)
        self.assertEqual(len(partner.user_ids), 2)

    def test_many2many_to_odoo_add_item(self):
        """Ensure adding new item will not remove the previous ones
        when Odoo receives a message.
        """

        # This converter wraps a user and adds info from its related partner.
        converter = Model(
            {
                "users": RelationToMany(
                    "user_ids",
                    "res.users",
                    Model(
                        {
                            "email": Field("email"),
                            "xref": Xref("base"),
                        },
                        __type__="user",
                    ),
                ),
                "xref": Xref("base"),
            },
        )

        partner = self.env.ref("base.main_partner")
        self.assertFalse(partner.user_ids)

        # Run our message reception.
        message: dict[str, Any] = {
            "users": [
                {
                    "__type__": "user",
                    "xref": "user_admin",
                },
            ],
            "xref": "main_partner",
        }
        message_to_odoo(self.env, message, self.env["res.partner"], converter)

        # Check the partner's users
        self.assertTrue(partner.user_ids)
        self.assertEqual(len(partner.user_ids), 1)

        message = {
            "users": [
                {
                    "__type__": "user",
                    "xref": "user_admin",
                },
                {
                    "__type__": "user",
                    "xref": "user_demo",
                },
            ],
            "xref": "main_partner",
        }
        message_to_odoo(self.env, message, self.env["res.partner"], converter)

        # Check the partner's users
        self.assertTrue(partner.user_ids)
        self.assertEqual(len(partner.user_ids), 2)

    def test_many2many_to_odoo_no___type__(self):
        """Ensure multiple sub-objects linked from the main one gets updated
        when Odoo receives a message.
        """

        # This converter wraps a user and adds info from its related partner.
        converter = Model(
            {
                "users": RelationToMany(
                    "user_ids",
                    "res.users",
                    Model(
                        {
                            "email": Field("email"),
                            "xref": Xref("base"),
                        },
                    ),
                ),
                "xref": Xref("base"),
            },
        )

        partner = self.env.ref("base.main_partner")
        self.assertFalse(partner.user_ids)

        # Run our message reception.
        message: dict[str, Any] = {
            "users": [
                {
                    "xref": "user_admin",
                },
                {
                    "xref": "user_demo",
                },
            ],
            "xref": "main_partner",
        }
        message_to_odoo(self.env, message, self.env["res.partner"], converter)

        # Check the partner's users
        self.assertTrue(partner.user_ids)
        self.assertEqual(len(partner.user_ids), 2)
