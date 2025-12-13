from __future__ import annotations

import datetime
import os
import typing

import amulet.core.version
import amulet.level.abc.registry
import amulet.level.bedrock.level_dat
import amulet.level.bedrock.raw_dimension
import amulet.leveldb
import amulet.utils.event
import amulet.utils.lock
import PIL.Image

__all__: list[str] = ["BedrockRawLevel"]

class BedrockRawLevel:
    @staticmethod
    def load(path: os.PathLike | str | bytes) -> BedrockRawLevel:
        """
        Load an existing Bedrock level from the given directory.
        Thread safe.
        """

    def close(self) -> None:
        """
        Close the level.
        closed event will be emitted when complete.
        External ReadWrite:Unique lock required.
        """

    def compact(self) -> None:
        """
        Compact the level.
        External Read:SharedReadWrite lock required.
        """

    def get_dimension(
        self, dimension_id: str | typing.SupportsInt
    ) -> amulet.level.bedrock.raw_dimension.BedrockRawDimension:
        """
        Get the raw dimension object for a specific dimension.
        External Read:SharedReadWrite lock required.
        """

    def is_open(self) -> bool:
        """
        Is the level open.
        External Read:SharedReadWrite lock required.
        """

    def is_supported(self) -> bool:
        """
        Is this level a supported version.
        This is true for all versions we support and false for snapshots and unsupported newer versions.
        TODO: thread safety
        """

    def open(self) -> None:
        """
        Open the level.
        opened event will be emitted when complete.
        External ReadWrite:Unique lock required.
        """

    def reload(self) -> None:
        """
        Reload the level.
        This is like closing and re-opening without releasing the session.lock file.
        External ReadWrite:Unique lock required.
        """

    def reload_metadata(self) -> None:
        """
        Reload the metadata. This can only be called when the level is closed.
        External ReadWrite:Unique lock required.
        """

    @property
    def biome_id_override(self) -> amulet.level.abc.registry.IdRegistry:
        """
        Overridden biome ids.
        External Read:SharedReadWrite lock required.
        """

    @property
    def block_id_override(self) -> amulet.level.abc.registry.IdRegistry:
        """
        Overridden block ids.
        External Read:SharedReadWrite lock required.
        """

    @property
    def closed(self) -> amulet.utils.event.Event[()]: ...
    @property
    def dimension_ids(self) -> list[str]:
        """
        The identifiers for all dimensions in this level.
        External Read:SharedReadWrite lock required.
        External Read:SharedReadOnly lock optional.
        """

    @property
    def last_opened_version(self) -> amulet.core.version.VersionNumber:
        """
        Getter:
        The game version that the level was last opened in.
        External Read:SharedReadWrite lock required.

        Setter:
        Set the maximum game version.
        If the game version is different this will call :meth:`reload`.
        External ReadWrite:SharedReadWrite lock required.
        """

    @last_opened_version.setter
    def last_opened_version(self, arg1: amulet.core.version.VersionNumber) -> None: ...
    @property
    def level_dat(self) -> amulet.level.bedrock.level_dat.BedrockLevelDat:
        """
        Getter:
        The NamedTag stored in the level.dat file. Returns a unique copy.
        External Read:SharedReadWrite lock required.

        Setter:
        Set the level.dat NamedTag
        This calls :meth:`reload` if the data version changed.
        External ReadWrite:Unique lock required.
        """

    @level_dat.setter
    def level_dat(
        self, arg1: amulet.level.bedrock.level_dat.BedrockLevelDat
    ) -> None: ...
    @property
    def level_name(self) -> str:
        """
        Getter:
        The name of the level.
        External Read:SharedReadWrite lock required.

        Setter:
        Set the level name.
        External ReadWrite:Unique lock required.
        """

    @level_name.setter
    def level_name(self, arg1: str) -> None: ...
    @property
    def leveldb(self) -> amulet.leveldb.LevelDB:
        """
        Get the LevelDB database.
        External Read::SharedReadWrite lock required.
        """

    @property
    def lock(self) -> amulet.utils.lock.OrderedLock:
        """
        The public lock
        Thread safe.
        """

    @property
    def modified_time(self) -> datetime.datetime:
        """
        The time when the level was lasted edited.
        External Read:SharedReadWrite lock required.
        """

    @property
    def opened(self) -> amulet.utils.event.Event[()]: ...
    @property
    def path(self) -> str:
        """
        The path to the level directory.
        Thread safe.
        """

    @property
    def platform(self) -> str:
        """
        The platform identifier. "bedrock"
        Thread safe.
        """

    @property
    def reloaded(self) -> amulet.utils.event.Event[()]: ...
    @property
    def thumbnail(self) -> PIL.Image.Image:
        """
        Get the thumbnail for the level.
        Thread safe.
        """
