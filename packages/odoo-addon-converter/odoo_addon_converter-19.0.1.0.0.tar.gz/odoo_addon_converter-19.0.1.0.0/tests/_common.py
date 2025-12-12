##############################################################################
#
#    Converter Odoo module
#    Copyright © 2025 XCG SAS <https://orbeet.io/>
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
import base64
import pkgutil

from odoo.addons.base.tests.common import BaseCommon, TransactionCaseWithUserDemo


class ConverterCase(BaseCommon):
    """Class with common setup."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a bank and partner (partially copied from demo data)
        cls.bank_bnp = cls.env["res.bank"].create([{"name": "BNP"}])
        data = pkgutil.get_data(
            "odoo.addons.base", "static/img/res_partner_1-image.png"
        )
        if data is None:
            cls.fail("Unable to read base module static/img/res_partner_1-image.png")
            return
        base64_content = base64.b64encode(data)
        cls.res_partner_1 = cls._create_partner(
            name="Wood Corner",
            # category_id=[
            #     Command.set(
            #         [
            #             cls.env.ref("base.res_partner_category_14").id,
            #             cls.env.ref("base.res_partner_category_12").id,
            #         ]
            #     )
            # ],
            is_company=True,
            street="1839 Arbor Way",
            city="Turlock",
            state_id=cls.env.ref("base.state_us_5").id,
            zip="95380",
            country_id=cls.env.ref("base.us").id,
            email="wood.corner26@example.com",
            phone="(623)-853-7197",
            website="http://www.wood-corner.com",
            image_1920=base64_content,
            vat="US12345672",
        )
        cls.env["ir.model.data"].create(
            [
                {
                    "module": "base",
                    "name": "bank_bnp",
                    "res_id": cls.bank_bnp.id,
                    "model": "res.bank",
                },
                {
                    "module": "base",
                    "name": "res_partner_1",
                    "res_id": cls.res_partner_1.id,
                    "model": "res.partner",
                },
            ]
        )


class TransactionCaseWithUserDemoXmlid(TransactionCaseWithUserDemo):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Add base.user_demo xref used in tests
        cls.env["ir.model.data"].create(
            [
                {
                    "module": "base",
                    "name": "user_demo",
                    "res_id": cls.user_demo.id,
                    "model": "res.users",
                },
            ]
        )
