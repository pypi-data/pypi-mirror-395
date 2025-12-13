from dataclasses import dataclass
from pathlib import Path

from plexutil.enums.file_type import FileType


@dataclass(frozen=True)
class LocalFileDTO:
    name: str
    extension: FileType
    location: Path

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LocalFileDTO):
            return False

        return (
            self.name == other.name
            and self.extension == other.extension
            and self.location == other.location
        )

    def __hash__(self) -> int:
        return hash((self.name, self.extension, self.location))
