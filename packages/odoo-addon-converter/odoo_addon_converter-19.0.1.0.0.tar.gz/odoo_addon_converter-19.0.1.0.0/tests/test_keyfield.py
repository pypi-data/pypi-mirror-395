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

from .. import KeyField, Model, Phase, RelationToOne, Skip
from .._context import ContextBuilder


class Test(tests.TransactionCase):
    def setUp(self):
        super().setUp()

        self.state_california = self.env.ref("base.state_us_5")
        self.state_cagliari = self.env.ref("base.state_it_ca")
        self.res_partner = self.env["res.partner"].create(
            {
                "name": "Awesome Animals",
                "is_company": True,
                "state_id": self.state_california.id,
                "zip": "95380",
                "country_id": self.env.ref("base.us").id,
                "email": "awesome.animals@example.com",
            }
        )

    def test_to_odoo(self):
        """Case when searching an instance with a key field."""
        converter = KeyField(
            "email",
            "res.partner",
        )

        # Email is unchanged.
        email = "awesome.animals@example.com"
        values = converter.message_to_odoo(
            self.env,
            {},
            Phase.UPDATE,
            email,
            self.res_partner,
            True,
        )

        self.assertEqual(values, Skip)

        # Email is unknown on phase PRECREATE, no given instance.
        email = "wood.corner27@example.com"
        values = converter.message_to_odoo(
            self.env,
            {},
            Phase.PRECREATE,
            email,
            None,
            True,
        )
        self.assertEqual(values, {"email": "wood.corner27@example.com"})

        # Email is changed on phase UPDATE, given instance.
        email = "wood.corner28@example.com"
        values = converter.message_to_odoo(
            self.env,
            {},
            Phase.UPDATE,
            email,
            self.res_partner,
            True,
        )
        self.assertEqual(values, {"email": "wood.corner28@example.com"})

    def test_lookup_scope(self):
        """Case when searching an instance with a key field but inside a scope."""
        email = "awesome.animals@example.com"
        converter = KeyField(
            "email",
            "res.partner",
            lookup_scope=lambda ctx, message: [("is_company", "=", ctx["is_company"])],
        )

        instance = converter.get_instance(self.env, {"is_company": True}, email)
        self.assertEqual(instance, self.res_partner)

        instance = converter.get_instance(self.env, {"is_company": False}, email)
        self.assertEqual(instance, None)

        self.res_partner.write({"is_company": False})
        instance = converter.get_instance(self.env, {"is_company": False}, email)
        self.assertEqual(instance, self.res_partner)

    def test_to_odoo_ctx_keys(self):
        """Test auto inherited context.
        Auto inherited context is a mechanism that allows any nested converter to
        ask for a context key that is not explicitly built and propagated from the
        root converter.
        The annotated "RelationToOne" converter build the context key "country_id"
        from the value of "country_code" received in the message.
        The "country_id" key is then injected into the context given to sub
        converters, in this case "KeyField".
        """

        converter = Model(
            {
                "state_code": Model.annotate(
                    to_odoo_context=ContextBuilder(
                        {
                            "country_id": ContextBuilder.computed(
                                lambda message: self.env["res.country"]
                                .search([("code", "=", message["country_code"])])
                                .id
                            ),
                        }
                    ),
                )(
                    RelationToOne(
                        "state_id",
                        "res.country.state",
                        KeyField(
                            "code",
                            "res.country.state",
                            lookup_scope=lambda ctx, message: [
                                ("country_id", "=", ctx["country_id"])
                            ],
                            to_odoo_ctx_keys=["country_id"],
                        ),
                    )
                ),
            }
        )

        # Search for California in US
        message = {
            "state_code": "CA",  # self.state_california.code
            "country_code": "US",  # self.state_california.country_id.code
        }
        values = converter.message_to_odoo(
            self.env,
            {},
            Phase.PRECREATE,
            message,
            None,
            True,
        )
        self.assertEqual(values, {"state_id": self.state_california.id})

        # Search for Cagliari in Italy
        message = {
            "state_code": "CA",  # self.state_cagliari.code
            "country_code": "IT",  # self.state_cagliari.country_id.code
        }
        values = converter.message_to_odoo(
            self.env,
            {},
            Phase.PRECREATE,
            message,
            None,
            True,
        )
        self.assertEqual(values, {"state_id": self.state_cagliari.id})
