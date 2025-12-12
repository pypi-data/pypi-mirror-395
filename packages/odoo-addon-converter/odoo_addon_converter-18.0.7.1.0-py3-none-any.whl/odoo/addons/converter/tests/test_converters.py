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

from odoo import tests  # type: ignore[import-untyped]

from ..base import Skip
from ..field import Field
from ..keyfield import KeyField
from ..model import Model
from ..relation import RelationToOne
from ..xref import Xref


class Test(tests.TransactionCase):
    """Test converter classes to convert between Odoo records & JSON dicts.
    See utils/converters.py.
    """

    def test_odoo_to_message(self):
        """Test conversion from an Odoo record to an Xbus message."""

        # Prepare our test record.
        user = self.env.user
        user.name = "test-name"
        user.country_id = self.env.ref("base.de")

        # Convert!
        payload = self._build_test_converter().odoo_to_message({}, user)
        self.assertIsNot(payload, Skip)

        # Grab xrefs that got built along with the payload; checked further.
        user_ref = self.env["ir.model.data"].object_to_xmlid(user)
        partner_ref = self.env["ir.model.data"].object_to_xmlid(user.partner_id)
        self.assertNotEqual(user_ref, partner_ref)

        # Check the payload.
        self.assertEqual(
            payload,
            {
                "__type__": "test-type",
                "country_code": "DE",
                "id": user_ref,
                "name": "test-name",
                "partner_id": partner_ref,
            },
        )

    def test_message_to_odoo(self):
        """Test conversion from an Xbus message to an Odoo record."""

        # The test record we are going to update here.
        user = self.env.user
        de_country = self.env.ref("base.de")
        self.assertNotEqual(user.name, "test-name")
        self.assertNotEqual(user.country_id.id, de_country.id)

        # Prepare an xref to reference our record.
        user_ref = self.env["ir.model.data"].object_to_xmlid(user)

        payload = {
            "__type__": "test-type",
            "country_code": "DE",
            "id": user_ref,
            "name": "test-name",
        }

        # Convert!
        changes = self._build_test_converter().message_to_odoo(
            self.env, {}, "update", payload, user
        )
        self.assertEqual(changes, {"country_id": de_country.id, "name": "test-name"})

        # Update our test record & check updated data.
        user.write(changes)
        self.assertEqual(user.name, "test-name")
        self.assertEqual(user.country_id.id, self.env.ref("base.de").id)

    @staticmethod
    def _build_test_converter():
        """Build a converter for our test record.
        Use converters of different kinds.
        """
        return Model(
            # TODO add a schema to test validation
            {
                "id": Xref(include_module_name=True),
                "country_code": RelationToOne(
                    "country_id", "res.country", KeyField("code", "res.country")
                ),
                "name": Field("name"),
                "partner_id": RelationToOne(
                    "partner_id", "res.partner", Xref(include_module_name=True)
                ),
            },
            __type__="test-type",
        )
