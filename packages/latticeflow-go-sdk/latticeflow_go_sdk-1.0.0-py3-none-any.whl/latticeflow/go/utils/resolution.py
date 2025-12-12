from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from typing import Callable

import yaml


SCHEMA_REGEXP = re.compile("[A-Za-z]+://")


def resolve_value(
    value: str,
    doc_path: Path,
    loc: str,
    yaml_loader: Callable[[Any], Any] = yaml.safe_load,
) -> dict:
    if value.startswith("#"):
        raise NotImplementedError(
            "References relative to schema root (i.e. starting with #) are not supported."
        )
    if SCHEMA_REGEXP.match(value):
        raise NotImplementedError("Remote references are not supported.")

    # Local file reference
    if Path(value).is_absolute():
        local_file_path = Path(value)
    else:
        local_file_path = Path(doc_path).parent / value

    try:
        with local_file_path.open() as f:
            inner = yaml_loader(f)
            return load_recursively(
                doc=inner, doc_path=local_file_path, loc=loc, yaml_loader=yaml_loader
            )
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Failed to resolve {loc}: {e}")


def load_recursively(
    doc: Any,
    doc_path: Path,
    loc: str = "",
    yaml_loader: Callable[[Any], Any] = yaml.safe_load,
) -> Any:
    if isinstance(doc, dict):
        value = None
        if "$ref" in doc:
            ref_value = doc.pop("$ref")
            value = resolve_value(ref_value, doc_path, loc, yaml_loader)

        result = {
            key: load_recursively(
                value,
                doc_path,
                loc=f"{loc}.{key}" if loc != "" else key,
                yaml_loader=yaml_loader,
            )
            for key, value in doc.items()
        }
        if value is not None:
            if isinstance(value, dict):
                result = {**result, **value}
            elif result == {}:
                return value
            else:
                prefix = f"Loading error for {loc}: " if loc != "" else ""

                raise ValueError(f"""{prefix}Cannot reference a non-dict value if other keys are present in the schema.
Referenced Value: {value}
Schema: {doc | {"$ref": ref_value}}
""")
        return result
    elif isinstance(doc, list):
        return [
            load_recursively(
                value, doc_path, loc=f"{loc}[{i}]", yaml_loader=yaml_loader
            )
            for i, value in enumerate(doc)
        ]
    else:
        return doc
