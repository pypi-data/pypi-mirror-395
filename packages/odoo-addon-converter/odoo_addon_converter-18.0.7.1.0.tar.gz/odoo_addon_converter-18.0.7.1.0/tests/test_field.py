##############################################################################
#
#    Converter Odoo module
#    Copyright © 2021, 2025 XCG SAS <https://orbeet.io/>
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

from .. import Field, Phase, TranslatedSelection


class Test(tests.TransactionCase):
    def setUp(self):
        super().setUp()
        self.active_user = self.env["res.users"].search(
            [("active", "=", True)], limit=1
        )
        self.inactive_user = self.env["res.users"].search(
            [("active", "=", False)], limit=1
        )

    def test_boolean_field(self):
        converter = Field("active")
        self.assertEqual(True, converter.odoo_to_message({}, self.active_user))
        self.assertEqual(False, converter.odoo_to_message({}, self.inactive_user))

        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, True, self.active_user, True
        )
        self.active_user.write(values)
        self.assertTrue(self.active_user.active)
        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, False, self.active_user, True
        )
        self.active_user.write(values)
        self.assertFalse(self.active_user.active)
        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, False, self.inactive_user, True
        )
        self.inactive_user.write(values)
        self.assertFalse(self.inactive_user.active)
        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, True, self.inactive_user, True
        )
        self.inactive_user.write(values)
        self.assertTrue(self.inactive_user.active)

    def test_message_formatter(self):
        # convert active boolean to those values
        active = "Active"
        inactive = "Inactive"

        # define some formatter
        def message_formatter(value: Any, is_blank: bool) -> Any:
            return active if value else inactive

        def odoo_formatter(value: Any):
            return value == active

        converter = Field(
            "active",
            message_formatter=message_formatter,
            odoo_formatter=odoo_formatter,
        )
        self.assertEqual(active, converter.odoo_to_message({}, self.active_user))
        self.assertEqual(inactive, converter.odoo_to_message({}, self.inactive_user))

        # already active, should be an empty dict
        self.assertEqual(
            {},
            converter.message_to_odoo(
                self.env, {}, Phase.UPDATE, active, self.active_user, True
            ),
        )
        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, inactive, self.active_user, True
        )
        self.active_user.write(values)
        self.assertFalse(self.active_user.active)

    def test_translated_selection(self):
        converter = TranslatedSelection("target", "en_US")
        self.assertEqual(
            "New Window",
            converter.odoo_to_message(
                {},
                self.env["ir.actions.act_url"].search(
                    [("target", "=", "new")], limit=1
                ),
            ),
        )
        self.assertEqual(
            "This Window",
            converter.odoo_to_message(
                {},
                self.env["ir.actions.act_url"].search(
                    [("target", "=", "self")], limit=1
                ),
            ),
        )

    def test_binary_data_uri(self):
        converter = Field("avatar_1920")
        partner = self.env.ref("base.partner_admin")
        old_image = partner.avatar_1920
        value = converter.odoo_to_message({}, partner)
        # admin partner avatar is stored with application/octet-stream
        self.assertTrue(value.startswith(b"data:application/octet-stream;base64,"))
        # white 1920x1920 image
        data_uri = """data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAB4AAAAeAAQAAAAAH2XdrAAAABGdBTUEAALGPC/xhBQAAACBjSFJN
AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAd2KE6QAAAAHdElN
RQfpAhURBCXSFMwjAAAIE0lEQVR42u3PAQ0AMAjAMPyb/mWQjE7BOu9Ysz0ADAwMDAwMfCfgesD1
gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOu
B1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5w
PeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA
6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64H
XA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA9
4HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDr
AdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdc
D7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3g
esD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB
1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wP
uB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6
wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHX
A64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4
HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA
9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcD
rgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7ge
cD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1
gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOu
B1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5w
PeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA
6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64H
XA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA9
4HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDr
AdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdc
D7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3g
esD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB
1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wP
uB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6
wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHX
A64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4
HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA
9YDrAdcDrgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcD
rgdcD7gecD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7ge
cD3gesD1gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1
gOsB1wOuB1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrAdcDrgdcD7gecD3gesD1gOsB1wOu
B1wPuB5wPeB6wPWA6wHXA64HXA+4HnA94HrA9YDrfdjxYRCgcj/RAAAAJXRFWHRkYXRlOmNyZWF0
ZQAyMDI1LTAyLTIxVDE3OjA0OjM3KzAwOjAw60rorAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNS0w
Mi0yMVQxNzowNDozNyswMDowMJoXUBAAAAAASUVORK5CYII="""
        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, data_uri, partner, True
        )
        partner.write(values)
        self.assertNotEqual(old_image, partner.avatar_1920)
        value = converter.odoo_to_message({}, partner)
        # not an attachment, mimetype is lost
        self.assertTrue(value.startswith(b"data:application/octet-stream;base64,"))
        converter = Field("image_1920")
        main_company = self.env.ref("base.main_company").partner_id
        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, data_uri, partner, True
        )
        main_company.write(values)
        value = converter.odoo_to_message({}, main_company)
        self.assertTrue(value.startswith(b"data:image/png;base64,"))
        # test on an attachment field
        data_uri = (
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElE"
            "QVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        )
        menu = self.env["ir.ui.menu"].search([], limit=1)
        old_image = menu.web_icon_data
        converter = Field("web_icon_data")
        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, data_uri, menu, True
        )
        menu.write(values)
        self.assertEqual(old_image, menu.web_icon_data)
        converter.post_hook(menu, data_uri)
        self.assertNotEqual(old_image, menu.web_icon_data)
        value = converter.odoo_to_message({}, menu)
        self.assertTrue(value.startswith(b"data:image/png;base64,"))

    def test_binary_data_uri_svg(self):
        """Test binary field with SVG image."""
        # Simple SVG data URI (unencoded)
        svg_content = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
            '<circle cx="5" cy="5" r="4" fill="red"/></svg>'
        )
        svg_data_uri = "data:image/svg+xml," + svg_content
        # Use a different menu than test_binary_data_uri to avoid conflicts
        menu = self.env["ir.ui.menu"].search([], limit=1, offset=1)
        old_image = menu.web_icon_data
        converter = Field("web_icon_data")
        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, svg_data_uri, menu, True
        )
        menu.write(values)
        self.assertEqual(old_image, menu.web_icon_data)
        converter.post_hook(menu, svg_data_uri)
        self.assertNotEqual(old_image, menu.web_icon_data)
        value = converter.odoo_to_message({}, menu)
        self.assertTrue(value.startswith(b"data:image/svg+xml;base64,"))
        # Verify non-admin user can read the attachment via converter
        demo_user = self.env.ref("base.user_demo")
        menu_demo = menu.with_user(demo_user)
        value_demo = converter.odoo_to_message({}, menu_demo)
        self.assertTrue(value_demo.startswith(b"data:image/svg+xml;base64,"))

    def test_binary_data_uri_text_plain(self):
        """Test binary field with text/plain content type."""
        # Simple text data URI (unencoded)
        text_data_uri = "data:text/plain,Hello World!"
        # Use a different menu than other tests to avoid conflicts
        menu = self.env["ir.ui.menu"].search([], limit=1, offset=2)
        old_data = menu.web_icon_data
        converter = Field("web_icon_data")
        values = converter.message_to_odoo(
            self.env, {}, Phase.UPDATE, text_data_uri, menu, True
        )
        menu.write(values)
        self.assertEqual(old_data, menu.web_icon_data)
        converter.post_hook(menu, text_data_uri)
        self.assertNotEqual(old_data, menu.web_icon_data)
        value = converter.odoo_to_message({}, menu)
        self.assertTrue(value.startswith(b"data:text/plain;base64,"))
