from __future__ import annotations

from typing import TYPE_CHECKING

import yaml
from wexample_helpers.const.types import PathOrString

if TYPE_CHECKING:
    from wexample_helpers_yaml.const.types import YamlContent, YamlContentDict


def yaml_fill_unresolved_vars(yml_text: str, fill_value: str | None = "") -> str:
    import re

    """
    Replace unresolved variable placeholders of the form ${VAR_NAME}
    in a YAML string with a specified fallback value (empty string by default).
    """
    # Pattern to match ${VAR} placeholders without nested braces
    unresolved_pattern = re.compile(r"\$\{([^}]+)\}")

    def replacer(match: re.Match) -> str:
        match.group(1)
        # Optionally, log or collect missing variables here
        return str(fill_value)

    return unresolved_pattern.sub(replacer, yml_text)


def yaml_read(
    file_path: PathOrString, default: YamlContent | None = None
) -> YamlContent | None:
    try:
        with open(file_path) as f:
            content = yaml.safe_load(f)

            if isinstance(content, dict):
                return content
            else:
                return default
    except Exception:
        return default


def yaml_read_dict(
    file_path: PathOrString, default: YamlContentDict | None = None
) -> YamlContentDict:
    content = yaml_read(file_path, default)

    if not content:
        return default or {}

    assert isinstance(content, dict)

    return content


def yaml_write(file_path: PathOrString, content: YamlContent) -> None:
    with open(file_path, "w") as f:
        yaml.safe_dump(content, f)
