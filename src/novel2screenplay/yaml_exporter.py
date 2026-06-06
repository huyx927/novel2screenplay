from __future__ import annotations

from typing import Any

import yaml


def to_yaml(data: dict[str, Any]) -> str:
    """Convert screenplay data to readable YAML text."""
    return yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    )


def from_yaml(yaml_text: str) -> dict[str, Any]:
    """Load YAML text back into a Python dictionary."""
    loaded = yaml.safe_load(yaml_text)

    if not isinstance(loaded, dict):
        raise ValueError("YAML 内容必须是一个对象。")

    return loaded