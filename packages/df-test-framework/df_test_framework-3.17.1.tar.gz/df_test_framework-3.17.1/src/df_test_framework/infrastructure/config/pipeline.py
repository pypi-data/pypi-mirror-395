"""
ConfigPipeline is responsible for loading configuration data from a sequence of
sources and merging them into a single dictionary that can be passed to a
Pydantic settings model.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from .sources import ConfigSource, merge_dicts


@dataclass
class ConfigPipeline:
    """
    Utility to serially execute configuration sources and merge the result.

    Later sources overwrite values from earlier ones, using deep merge semantics
    for nested dictionaries.
    """

    sources: list[ConfigSource] = field(default_factory=list)

    def extend(self, sources: Iterable[ConfigSource]) -> ConfigPipeline:
        self.sources.extend(sources)
        return self

    def prepend(self, *sources: ConfigSource) -> ConfigPipeline:
        self.sources = list(sources) + self.sources
        return self

    def add(self, source: ConfigSource) -> ConfigPipeline:
        self.sources.append(source)
        return self

    def load(self) -> dict:
        merged: dict = {}
        for source in self.sources:
            data = source.load()
            merged = merge_dicts(merged, data)
        return merged

    def load_into(self, target: Mapping) -> dict:
        merged = dict(target)
        for source in self.sources:
            data = source.load()
            merged = merge_dicts(merged, data)
        return merged
