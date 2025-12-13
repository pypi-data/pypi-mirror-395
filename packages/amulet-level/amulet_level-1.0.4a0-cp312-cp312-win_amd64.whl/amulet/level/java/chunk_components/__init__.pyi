from __future__ import annotations

import collections.abc
import typing

import amulet.nbt

__all__: list[str] = ["DataVersionComponent", "JavaRawChunkComponent"]

class DataVersionComponent:
    ComponentID: typing.ClassVar[str] = "Amulet::DataVersionComponent"
    @property
    def data_version(self) -> int: ...

class JavaRawChunkComponent:
    ComponentID: typing.ClassVar[str] = "Amulet::JavaRawChunkComponent"
    @property
    def raw_data(self) -> collections.abc.MutableMapping[str, amulet.nbt.NamedTag]:
        """
        This is subject to change as data gets moved into the chunk class.
        Do not rely on data in here existing.
        """

    @raw_data.setter
    def raw_data(
        self, arg1: collections.abc.Mapping[str, amulet.nbt.NamedTag]
    ) -> None: ...
