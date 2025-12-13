from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexutil.enums.library_type import LibraryType


class LibraryOpError(Exception):
    def __init__(
        self,
        op_type: str,
        library_type: LibraryType,
        description: str = "",
    ) -> None:
        self.op_type = op_type
        self.library_type = library_type
        self.description = description

        message = (
            self.op_type
            + ": "
            + self.library_type.value
            + " | "
            + self.description
        )

        super().__init__(message)
