from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from amulet.core.version import VersionNumber

if TYPE_CHECKING:
    from .block import BlockData
    from .biome import BiomeData


class GameVersion(ABC):
    @abstractmethod
    def supports_version(self, platform: str, version: VersionNumber) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def platform(self) -> str:
        """The platform string this instance is part of."""
        raise NotImplementedError

    @property
    @abstractmethod
    def min_semantic_version(self) -> VersionNumber:
        """
        The minimum semantic version this instance can be used with.

        >>> game_version: GameVersion
        >>> game_version.min_semantic_version
        VersionNumber(1, 21, 9)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def max_known_semantic_version(self) -> VersionNumber:
        """
        The maximum known semantic version this instance can be used with.
        This instance may be compatible with higher versions but this is the highest it is known to work with.

        >>> game_version: GameVersion
        >>> game_version.max_known_semantic_version
        VersionNumber(1, 21, 9)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def max_semantic_version(self) -> VersionNumber:
        """
        The maximum semantic version this instance should accept.
        Note that this is usually not a valid version.

        >>> game_version: GameVersion
        >>> game_version.max_semantic_version
        VersionNumber(1, 22, 10, -1)
        VersionNumber(2, -1)  # This is used in the newest version.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def min_block_version(self) -> VersionNumber:
        """
        The minimum block version this instance can be used with.

        >>> game_version: GameVersion
        >>> game_version.min_block_version
        # Java - data version
        VersionNumber(4553)  # 1.21.9 Release Candidate 1
        # Bedrock - uint8[4] interpreted as uint32
        VersionNumber(18168865)  # 1.21.60.33
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def max_known_block_version(self) -> VersionNumber:
        """
        The maximum known block version this instance can be used with.
        This instance may be compatible with higher versions but this is the highest it is known to work with.

        >>> game_version: GameVersion
        >>> game_version.max_known_block_version
        # Java - data version
        VersionNumber(4554)  # 1.21.9
        # Bedrock - uint8[4] interpreted as uint32
        VersionNumber(18168865)  # 1.21.60.33
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def max_block_version(self) -> VersionNumber:
        """
        The maximum block version this instance should accept.
        Note that this is usually not a valid version.

        >>> game_version: GameVersion
        >>> game_version.max_block_version
        # Java - data version
        VersionNumber(4554)  # Java Edition 1.21.9
        VersionNumber(2147483647)  # The newest version uses max(int32) to catch all future versions.
        # Bedrock - uint8[4] interpreted as uint32
        VersionNumber(18168865)  # 1.21.60.33
        VersionNumber(4294967295)  # The newest version uses max(uint32) to catch all future versions.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def block(self) -> BlockData:
        raise NotImplementedError

    @property
    @abstractmethod
    def biome(self) -> BiomeData:
        raise NotImplementedError
