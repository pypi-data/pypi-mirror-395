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

from .._context import ContextBuilder, build_context


class Test(tests.TransactionCase):
    def setUp(self):
        super().setUp()

        # Some of the attributes for res_partner_1 are
        # name = "Wood Corner"
        # is_company = True
        # street = "1839 Arbor Way"
        # state_id = self.env.ref("base.state_us_5")
        # email = "wood.corner26@example.com"
        # image_1920 = file("base/static/img/res_partner_1-image.png")
        self.res_partner_1 = self.env.ref("base.res_partner_1")

    def test_to_message_context(self):
        """Case when context is built from instance."""
        ctx_builder = ContextBuilder(
            {
                "id": ContextBuilder.instance_id(),
                "name": ContextBuilder.instance_attr("name"),
                "is_company": ContextBuilder.instance_attr("is_company"),
                "address": ContextBuilder.computed(
                    lambda instance: f"{instance.street} {instance.state_id.name}"
                ),
                "quote": ContextBuilder.const(
                    "When in doubt or danger, run in circles, scream and shout."
                ),
            }
        )
        ctx = build_context(
            ctx_builder,
            {},
            self.res_partner_1,
            None,
        )
        self.assertEqual(
            ctx,
            {
                "id": self.res_partner_1.id,
                "name": self.res_partner_1.name,
                "is_company": self.res_partner_1.is_company,
                "address": "1839 Arbor Way California",
                "quote": "When in doubt or danger, run in circles, scream and shout.",
            },
        )

    def test_to_odoo_context(self):
        """Case when context is built from message."""
        ctx_builder = ContextBuilder(
            {
                "partner_id": ContextBuilder.computed(
                    lambda message: self.env.ref(message.get("id")).id
                ),
                "name": ContextBuilder.from_message("name"),
            }
        )
        message_value = {
            "id": "base.res_partner_1",
            "name": "Partner 1",
            "is_company": False,
            "street": "1840 Arbor Way",
            "email": "wood.corner27@example.com",
        }
        ctx = build_context(
            ctx_builder,
            {},
            None,
            message_value,
        )
        self.assertEqual(
            ctx,
            {
                "partner_id": self.res_partner_1.id,
                "name": "Partner 1",
            },
        )

    def test_inherit_parent_context_subset(self):
        """Case when we only want a subset of the parent context."""
        ctx_builder = ContextBuilder(inherit=["partner_id", "name"])
        ctx_parent = {
            "partner_id": 1,
            "name": "Partner 1",
            "email": "wood.corner27@example.com",
        }
        ctx = build_context(
            ctx_builder,
            ctx_parent,
            None,
            None,
        )
        self.assertEqual(
            ctx,
            {
                "partner_id": 1,
                "name": "Partner 1",
            },
        )

    def test_inherit_parent_context_variable(self):
        """Case when we want specific variables from the parent context."""
        ctx_builder = ContextBuilder(
            {
                "partner_name": ContextBuilder.from_parent("name"),
                "email": ContextBuilder.inherit,
            }
        )
        ctx_parent = {
            "partner_id": 1,
            "name": "Partner 1",
            "email": "wood.corner27@example.com",
        }
        ctx = build_context(
            ctx_builder,
            ctx_parent,
            None,
            None,
        )
        self.assertEqual(
            ctx,
            {
                "partner_name": "Partner 1",
                "email": "wood.corner27@example.com",
            },
        )

    def test_inherited(self):
        ctx_builder = ContextBuilder(
            {
                "partner_name": ContextBuilder.from_parent("name"),
                "email": ContextBuilder.inherit,
                "name": ContextBuilder.const("John Doe"),
            },
            inherit=["car"],
        )

        self.assertEqual(set(ctx_builder.inherited()), set(["car", "name", "email"]))

    def test_inherit_if_missing(self):
        ctx_builder = ContextBuilder(
            {
                "partner_name": ContextBuilder.from_parent("name"),
                "email": ContextBuilder.inherit,
                "friend": ContextBuilder.const("John Doe"),
            },
            inherit=["car"],
        )

        ctx_builder.inherit_if_missing(["another", "friend"])

        self.assertEqual(
            set(ctx_builder.inherited()),
            set(["car", "name", "email", "another"]),
        )
