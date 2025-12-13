from plexutil.enums.library_type import LibraryType


class LibraryUnsupportedError(Exception):
    def __init__(
        self,
        op_type: str,
        library_type: LibraryType,
    ) -> None:
        self.op_type = op_type
        self.library_type = library_type
        message = self.op_type + ": " + library_type.value
        super().__init__(message)
