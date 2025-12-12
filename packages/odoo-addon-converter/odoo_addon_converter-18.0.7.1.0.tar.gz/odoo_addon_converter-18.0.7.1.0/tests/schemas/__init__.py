import json
import pkgutil
from collections.abc import Iterator
from typing import Any


def get_schemas() -> Iterator[Any]:
    for file_prefix in ("product",):
        data: bytes | None = pkgutil.get_data(__name__, f"{file_prefix}.schema.json")
        if data:
            yield json.loads(data)
