##############################################################################
#
#    Converter Odoo module
#    Copyright © 2021 XCG SAS <https://orbeet.io/>
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

from .. import Field, Model, Switch
from ._common import ConverterCase


def falser(*a, **kw) -> bool:
    return False


class Test(ConverterCase):
    def test_to_message(self):
        # first make sure we have an instance to test on
        self.assertTrue(self.env.ref("base.bank_bnp").active)

        converter = Switch(
            [
                (
                    lambda e: e.active,
                    falser,
                    Model(
                        {"name": Field("name"), "active": Field("active")},
                        __type__="__activebanks__",
                    ),
                ),
                (
                    None,
                    falser,
                    Model(
                        {"name": Field("name"), "active": Field("active")},
                        __type__="__inactivebanks__",
                    ),
                ),
            ]
        )

        msg = converter.odoo_to_message({}, self.env.ref("base.bank_bnp"))
        self.assertEqual("__activebanks__", msg.get("__type__"))
