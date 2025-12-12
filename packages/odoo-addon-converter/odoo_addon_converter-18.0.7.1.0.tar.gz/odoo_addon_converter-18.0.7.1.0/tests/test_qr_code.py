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

from unittest import skipUnless

from odoo import tests  # type: ignore[import-untyped]

from ..qr_code import QRCodeDataURL, QRCodeFile, stringToQRCode


@skipUnless(tests.can_import("qrcode"), "qrcode module not available")
class TestQRCode(tests.TransactionCase):
    def setUp(self):
        super().setUp()
        self.ready_mat = self.env["res.partner"].search(
            [("name", "=", "Ready Mat")], limit=1
        )

    def test_print_qr_code_1(self):
        qr = stringToQRCode("https://google.com")
        qr.print_ascii()

    def test_string_to_qr_code_2(self):
        qr = stringToQRCode(self.ready_mat.website)
        qr.print_ascii()

    def test_qr_code_file(self):
        converter = QRCodeFile("website")
        img = converter.odoo_to_message({}, self.ready_mat)

        self.assertEqual("image/png", img["mime-type"])
        self.assertRegex(
            img["body"],
            r"[A-Za-z0-9+/=]+$",
            "The generated base64 body is incorrect",
        )

    def test_qr_code_data_url(self):
        converter = QRCodeDataURL("website")
        url = converter.odoo_to_message({}, self.ready_mat)
        self.assertRegex(
            url,
            r"^data:image/png;base64,[A-Za-z0-9+/=]+$",
            "The generated Data URL is not correctly formatted",
        )
