##############################################################################
#
#    Converter Odoo module
#    Copyright © 2023, 2024 XCG SAS <https://orbeet.io/>
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

from odoo.tests import tagged

from ..mail_template import MailTemplate
from ._common import ConverterCase, TransactionCaseWithUserDemoXmlid


@tagged("-standard", "odoo_addons_mail")
class Test(ConverterCase, TransactionCaseWithUserDemoXmlid):
    """Test converter that wraps ``mail.template::_render_template``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_admin = cls.env.ref("base.user_admin")

    def test_mail_template_odoo_to_message(self):
        converter = MailTemplate("hello {{ object.login }}")
        converted = converter.odoo_to_message({}, self.user_demo)
        self.assertEqual(converted, "hello demo")

    def test_mail_template_odoo_to_message_multiple_records(self):
        converter = MailTemplate(
            "hello {{ ' & '.join(ctx['records'].sorted('login').mapped('login')) }}"
        )
        converted = converter.odoo_to_message({}, self.user_admin | self.user_demo)
        self.assertEqual(converted, "hello admin & demo")
