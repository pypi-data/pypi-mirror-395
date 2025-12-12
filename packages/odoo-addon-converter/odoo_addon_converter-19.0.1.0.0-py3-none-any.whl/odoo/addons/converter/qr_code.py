##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020, 2025 XCG SAS <https://orbeet.io/>
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
import io
from typing import Any

from odoo import models  # type: ignore[import-untyped]

from .base import Context, Converter

_qrcode: None | Exception = None
try:
    import qrcode  # type: ignore[import-untyped]
except ImportError as e:
    _qrcode = e


def QRToImage(qr):
    """Generate a image dict from a QR Code"""
    img = qr.make_image(fill="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")

    body = base64.b64encode(buffered.getvalue()).decode("ascii")
    return {"body": body, "mime-type": "image/png"}


def stringToQRCode(data: str):
    """Generate a QR code from a string and return it as a base64-encoded image."""
    if not data:
        return False

    if _qrcode is not None:
        raise _qrcode

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr


class QRCodeFile(Converter):
    def __init__(self, fieldname):
        super().__init__()
        self.fieldname = fieldname

    def odoo_to_message(self, ctx: Context, instance: models.Model) -> Any:
        value = getattr(instance, self.fieldname)

        if not value:
            return {}

        return QRToImage(stringToQRCode(value))


class QRCodeDataURL(Converter):
    def __init__(self, fieldname):
        super().__init__()
        self.fieldname = fieldname

    def odoo_to_message(self, ctx: Context, instance: models.Model) -> Any:
        value = getattr(instance, self.fieldname)

        if not value:
            return ""

        image = QRToImage(stringToQRCode(value))
        return "data:{};base64,{}".format(
            image["mime-type"],
            image["body"],
        )
