##############################################################################
#
#    Converter Odoo module
#    Copyright © 2020, 2025 XCG Consulting <https://xcg-consulting.fr>
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
import datetime
from collections.abc import Callable
from typing import Any, Literal
from urllib.parse import urlsplit
from urllib.request import urlopen

from odoo import api, fields, models

from .base import Context, Newinstance, Phase, PostHookConverter, Skip, SkipType


class Field(PostHookConverter):
    """Converter linked to a single field"""

    def __init__(
        self,
        field_name: str,
        default: Any = None,
        send_empty: bool = True,
        required_blank_value: Any = None,
        message_formatter: Callable[[Any, bool], Any] | None = None,
        odoo_formatter: Callable[[Any], Any] | None = None,
    ):
        """
        :param field_name: name of the field on the instance
        :param default: a default value when the field is absent from the
        message. Useful when the default value is different that odoo’s
        default, like on active fields.
        :param send_empty: False when the field should be skip
        :param required_blank_value: indicates that the field is required in
        the message, and provided a value to replace any empty value given by
        Odoo
        :param message_formatter: method that will be used to format the value
        in the message. Signature should be (value: Any, is_blank: bool).
        In the case of datetime and date, isoformat will not be used if this is
        defined.
        :param odoo_formatter: method that will be used to format the value
        for odoo.
        """
        super().__init__()
        self.field_name = field_name
        self.default = default
        self.send_empty = send_empty or required_blank_value is not None
        self.required_blank_value = required_blank_value
        self._blank_value: Literal[False, "", 0] | list | float | None = None
        self._message_formatter = message_formatter
        self._odoo_formatter = odoo_formatter

    def blank_value(self, instance):
        if self.required_blank_value is not None:
            return self.required_blank_value
        if self._blank_value is not None:
            return self._blank_value

        field = instance._fields[self.field_name]
        if field.type == "boolean":
            self._blank_value = False
        elif field.type == "many2one":
            self._blank_value = ""
        elif field.type == ("monetary", "integer"):
            self._blank_value = 0
        elif field.type == "float":
            self._blank_value = 0.0
        elif field.type in ("one2many", "many2many"):
            self._blank_value = []
        else:
            self._blank_value = ""

        return self._blank_value

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        value = False
        # could be empty due to chaining converter on a many2one without value
        # for example
        if instance:
            value = getattr(instance, self.field_name)
        # odoo returns False rather than None
        if value is False:
            if self.send_empty:
                blank = self.blank_value(instance)
                if self._message_formatter:
                    blank = self._message_formatter(blank, True)
                return blank
            return Skip
        if isinstance(value, datetime.datetime):
            value = instance.env.tz
            if not self._message_formatter:
                value = value.isoformat()
        if isinstance(value, datetime.date):
            if not self._message_formatter:
                value = value.isoformat()
        field = instance._fields[self.field_name]
        if isinstance(field, fields.Binary):
            if field.attachment:
                domain = [
                    ("res_model", "=", instance._name),
                    ("res_field", "=", self.field_name),
                    ("res_id", "in", instance.ids),
                ]
                # sudo needed, no right to read those attachments
                attachment = instance.env["ir.attachment"].sudo().search(domain)
                mimetype = attachment.mimetype.encode("UTF-8")
            else:
                mimetype = b"application/octet-stream"
            value = b"data:" + mimetype + b";base64," + value
        if self._message_formatter:
            value = self._message_formatter(value, False)
        return value

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        ctx: Context,
        phase: Phase.Type,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        if phase == Phase.POSTCREATE:
            return {}
        if not value_present:
            # No value set in the message
            if self.default is None:
                return {}
            message_value = self.default
        # do not include value if already the same
        if instance and instance is not Newinstance:
            value = self.odoo_to_message(ctx, instance)
            if isinstance(value, SkipType) or value == message_value:
                return {}
        if instance:
            field = instance._fields[self.field_name]
            if isinstance(field, fields.Binary):
                if field.attachment:
                    return {}
                else:
                    url = urlsplit(message_value)
                    if url.scheme != "data":
                        # urlsplit raises ValueError too
                        raise ValueError("Not a Data URI (%s scheme)", url.scheme)
                    with urlopen(message_value, timeout=1) as response:
                        message_value = base64.b64encode(response.read())

        if self._odoo_formatter:
            message_value = self._odoo_formatter(message_value)

        return {self.field_name: message_value}

    def post_hook(self, instance: models.BaseModel, message_data):
        if instance:
            field = instance._fields[self.field_name]
            if isinstance(field, fields.Binary):
                if field.attachment:
                    # create or update ir.attachment directly
                    url = urlsplit(message_data)
                    # sudo needed, no right to read those attachments
                    if url.scheme != "data":
                        # urlsplit raises ValueError too
                        raise ValueError("Not a Data URI (%s scheme)", url.scheme)
                    domain = [
                        ("res_model", "=", instance._name),
                        ("res_field", "=", self.field_name),
                        ("res_id", "in", instance.ids),
                    ]
                    # sudo needed, no right to read those attachments
                    Attachment = instance.env["ir.attachment"].sudo()
                    attachment = Attachment.search(domain)
                    with urlopen(message_data, timeout=1) as response:
                        datas = base64.b64encode(response.read())
                    if self._odoo_formatter:
                        datas = self._odoo_formatter(datas)
                    # Extract mimetype from data URI path
                    # e.g., "image/png;base64,..." or "text/plain,..."
                    path_part = url.path.split(",", 1)[0]  # Remove data content
                    mimetype = path_part.split(";", 1)[0]  # Remove ";base64" etc.
                    if attachment:
                        attachment.write({"datas": datas, "mimetype": mimetype})
                    else:
                        # Create attachment if it doesn't exist
                        Attachment.create(
                            {
                                "name": self.field_name,
                                "res_model": instance._name,
                                "res_field": self.field_name,
                                "res_id": instance.id,
                                "type": "binary",
                                "datas": datas,
                                "mimetype": mimetype,
                            }
                        )
                    instance.invalidate_recordset([self.field_name])


class TranslatedSelection(Field):
    """Converter that uses a translation value of a selection field rather
    than its technical value.
    In messages, this converter should not be used, prefer to use the technical
    value over translation.
    """

    def __init__(
        self,
        field_name: str,
        language: str,
        default: Any = None,
        send_empty: bool = True,
        required_blank_value: Any = None,
    ):
        if not language:
            raise ValueError("language must have a value")
        super().__init__(field_name, default, send_empty, required_blank_value)
        self._language = language

    def _lazy_dicts(self, instance: models.BaseModel):
        if not hasattr(self, "_lazy_dict_odoo_to_message"):
            description_selection = (
                instance.with_context(lang=self._language)
                ._fields[self.field_name]
                ._description_selection(instance.env)
            )
            self._lazy_dict_odoo_to_message = dict(description_selection)
            self._lazy_dict_message_to_odoo = dict(
                (b, a) for a, b in description_selection
            )

    def odoo_to_message(self, ctx: Context, instance: models.BaseModel) -> Any:
        value = super().odoo_to_message(ctx, instance)
        if value:
            self._lazy_dicts(instance)
            value = self._lazy_dict_odoo_to_message.get(value)
        return value

    def message_to_odoo(
        self,
        odoo_env: api.Environment,
        ctx: Context,
        phase: Phase.Type,
        message_value: Any,
        instance: models.BaseModel,
        value_present: bool = True,
    ) -> dict | SkipType:
        message = super().message_to_odoo(
            odoo_env, ctx, phase, message_value, instance, value_present
        )
        if not isinstance(message, SkipType) and self.field_name in message:
            self._lazy_dicts(instance)
            message[self.field_name] = self._lazy_dict_message_to_odoo.get(
                message[self.field_name]
            )
        return message
