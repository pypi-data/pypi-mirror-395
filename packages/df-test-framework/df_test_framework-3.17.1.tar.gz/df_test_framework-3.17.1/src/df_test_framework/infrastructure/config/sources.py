"""
Configuration sources produce dictionaries that can be merged into settings.
"""

from __future__ import annotations

import os
import sys
from collections.abc import Iterable, Mapping, MutableMapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from dotenv import dotenv_values

NestedKeySeparator = "__"


class ConfigSource(Protocol):
    """Protocol implemented by configuration sources."""

    def load(self) -> dict[str, Any]: ...


def merge_dicts(base: Mapping[str, Any], update: Mapping[str, Any]) -> dict[str, Any]:
    """
    Deep merge two dictionaries, returning a new dict.
    """
    result: dict[str, Any] = dict(base)
    for key, value in update.items():
        if key in result and isinstance(result[key], MutableMapping) and isinstance(value, Mapping):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def _to_nested(key: str, value: Any, *, delimiter: str = NestedKeySeparator) -> dict[str, Any]:
    parts = key.split(delimiter)
    nested: dict[str, Any] = {}
    current = nested
    for part in parts[:-1]:
        current[part.lower()] = {}
        current = current[part.lower()]
    current[parts[-1].lower()] = value
    return nested


def _normalise_key(key: str) -> str:
    return key.strip().lower()


@dataclass
class DictSource(ConfigSource):
    """
    Simple source backed by a dictionary (used for overrides).
    """

    data: Mapping[str, Any]

    def load(self) -> dict[str, Any]:
        return dict(self.data)


@dataclass
class EnvVarSource(ConfigSource):
    """
    Load configuration from environment variables.

    Uses the same semantics as pydantic-settings: prefix with APP_ by default,
    nested keys separated by double underscore.
    """

    prefix: str = "APP_"
    delimiter: str = NestedKeySeparator
    environ: Mapping[str, str] = field(default_factory=lambda: os.environ)

    def load(self) -> dict[str, Any]:
        collected: dict[str, Any] = {}
        for key, value in self.environ.items():
            if not key.startswith(self.prefix):
                continue
            stripped = key[len(self.prefix) :]
            nested = _to_nested(stripped, value, delimiter=self.delimiter)
            collected = merge_dicts(collected, nested)

        # Support environment override for namespace selection
        if "ENV" in self.environ:
            collected = merge_dicts(collected, {"env": self.environ["ENV"].lower()})

        return collected


@dataclass
class DotenvSource(ConfigSource):
    """
    Load configuration from one or multiple .env files.
    """

    files: Iterable[Path]
    encoding: str = "utf-8"
    override: bool = False

    def load(self) -> dict[str, Any]:
        merged: dict[str, Any] = {}
        for file in self.files:
            if not file.exists():
                continue
            values = dotenv_values(dotenv_path=file, encoding=self.encoding)
            for key, value in values.items():
                if value is None:
                    continue
                nested = _to_nested(key, value)
                if self.override:
                    merged = merge_dicts(merged, nested)
                else:
                    merged = merge_dicts(nested, merged)
        return merged


@dataclass
class ArgSource(ConfigSource):
    """
    Parse command line arguments of the form --APP_FOO__BAR=value.
    """

    argv: Iterable[str] = field(default_factory=lambda: sys.argv[1:])
    prefix: str = "APP_"
    delimiter: str = NestedKeySeparator

    def load(self) -> dict[str, Any]:
        merged: dict[str, Any] = {}
        for arg in self.argv:
            if not arg.startswith("--"):
                continue
            if "=" not in arg:
                continue
            name, value = arg[2:].split("=", 1)
            if not name.startswith(self.prefix):
                continue
            stripped = name[len(self.prefix) :]
            nested = _to_nested(stripped, value, delimiter=self.delimiter)
            merged = merge_dicts(merged, nested)
        return merged
