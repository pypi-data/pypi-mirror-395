##############################################################################
#
#    Converter Odoo module
#    Copyright © 2024 XCG SAS <https://orbeet.io/>
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
import json
from unittest import skipUnless

from odoo import tests  # type: ignore[import-untyped]

from ..validate import Validator


@skipUnless(tests.can_import("fastjsonschema"), "fastjsonschema module not available")
class TestValidate(tests.TransactionCase):
    def test_validate(self):
        validator = Validator(
            "odoo.addons.converter.tests.schemas", "https://example.com/{}.schema.json"
        )
        validator.initialize()
        validator.validate(
            "product",
            json.loads("""{
  "productId": 1,
  "productName": "An ice sculpture",
  "price": 12.5,
  "tags": [
    "cold",
    "ice"
  ]
}"""),
        )

    def test_validate_dir(self):
        validator = Validator(
            "odoo.addons.converter.tests",
            "https://example.com/{}.schema.json",
            "schemas_dir",
        )
        validator.initialize()
        validator.validate(
            "product",
            json.loads("""{
  "productId": 1,
  "productName": "An ice sculpture",
  "price": 12.5,
  "tags": [
    "cold",
    "ice"
  ]
}"""),
        )
