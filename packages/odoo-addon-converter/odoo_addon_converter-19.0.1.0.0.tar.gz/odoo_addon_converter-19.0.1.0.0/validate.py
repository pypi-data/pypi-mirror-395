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
import json
import logging
import os
from collections.abc import Callable
from enum import StrEnum
from importlib import import_module
from typing import Any, LiteralString

from odoo import _
from odoo.exceptions import UserError

_fastjsonschema: None | Exception = None
try:
    import fastjsonschema  # type: ignore[import-untyped]
except ImportError as e:
    _fastjsonschema = e


_logger = logging.getLogger(__name__)


class Validation(StrEnum):
    """Type of validation"""

    SKIP = "skip"
    SOFT = "soft"
    STRICT = "strict"


class NotInitialized(Exception):
    pass


def _add_schema(schemas, schema):
    if "$id" in schema:
        schemas[schema["$id"]] = schema
    else:
        _logger.warning("Schema without $id (schema ignored)")


class Validator:
    def __init__(
        self,
        package_name: str,
        default_url_pattern: str,
        directory: str | None = None,
    ):
        """
        :param package_name: Package where the schema can be found
        :param default_url_pattern: pattern for url ({} will be replaced by $id)
        :param directory: directory to search for json, not used if a get_schema is
        provided in the package.
        """
        self.package_name = package_name
        # exemple "https://annonces-legales.fr/xbus/schemas/v1/{}.schema.json"
        self.default_url_pattern = default_url_pattern
        self.validators: dict[LiteralString, Callable] = {}
        self.initialized = False
        self.encoding = "UTF-8"
        self.directory = directory

    def initialize(self) -> None:
        if self.initialized:
            return
        schemas: dict[LiteralString, Any] = {}
        module = import_module(self.package_name)
        if hasattr(module, "get_schemas"):
            for schema in module.get_schemas():
                _add_schema(schemas, schema)
        else:
            if module.__file__ is None:
                # XXX maybe not the best type of error
                raise UserError(_("Module %s has no file", self.package_name))
            # Fallback on searching schema json files
            schema_search_path = os.path.dirname(module.__file__)
            schema_search_path = os.path.abspath(
                os.path.join(schema_search_path, self.directory)
                if self.directory is not None
                else schema_search_path
            )
            for root, _dirs, files in os.walk(schema_search_path):
                for fname in files:
                    fpath = os.path.join(root, fname)
                    if fpath.endswith((".json",)):
                        with open(fpath, encoding=self.encoding) as schema_fd:
                            schema = json.load(schema_fd)
                            _add_schema(schemas, schema)

        # Prepare validators for each schema. We add an HTTPS handler that
        # points back to our schema definition cache built above.
        for schema_id, schema in schemas.items():
            if _fastjsonschema is not None:
                raise _fastjsonschema
            self.validators[schema_id] = fastjsonschema.compile(
                schema,
                handlers={"https": lambda uri: schemas[uri]},
                use_default=False,
            )
        self.initialized = True

    def validate(self, schema_id: str, payload) -> None:
        if not self.initialized:
            raise NotInitialized("please call the initialize() method")

        self.validators[self.default_url_pattern.format(schema_id)](payload)
