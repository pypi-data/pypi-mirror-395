from __future__ import annotations

from amulet.level.abc.level import Level
from amulet.level.loader import NoValidLevelLoader, get_level

from . import _amulet_level, _version, abc, bedrock, java, loader

__all__: list[str] = [
    "Level",
    "NoValidLevelLoader",
    "abc",
    "bedrock",
    "compiler_config",
    "get_level",
    "java",
    "loader",
]

def _init() -> None: ...

__version__: str
compiler_config: dict
