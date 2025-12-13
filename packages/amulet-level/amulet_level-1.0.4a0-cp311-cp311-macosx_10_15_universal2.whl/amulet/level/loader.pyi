from __future__ import annotations

import os
import pathlib
import types
import typing

import amulet.level.abc.level

__all__: list[str] = [
    "LevelLoaderPathToken",
    "LevelLoaderToken",
    "NoValidLevelLoader",
    "get_level",
]

class LevelLoaderPathToken(LevelLoaderToken):
    def __init__(self, arg0: os.PathLike | str | bytes) -> None: ...

class LevelLoaderToken:
    @typing.overload
    def __eq__(self, other: LevelLoaderToken) -> bool: ...
    @typing.overload
    def __eq__(self, other: typing.Any) -> bool | types.NotImplementedType: ...
    def __hash__(self) -> int: ...
    def repr(self) -> str: ...

class NoValidLevelLoader(Exception):
    pass

@typing.overload
def get_level(token: LevelLoaderToken) -> amulet.level.abc.level.Level: ...
@typing.overload
def get_level(path: pathlib.Path) -> amulet.level.abc.level.Level: ...
