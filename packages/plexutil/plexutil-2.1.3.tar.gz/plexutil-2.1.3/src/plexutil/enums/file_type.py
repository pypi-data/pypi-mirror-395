from __future__ import annotations

from enum import Enum


class FileType(Enum):
    MP3 = "mp3"
    MP4 = "mp4"
    AAC = "aac"
    OGG = "ogg"
    WMA = "wma"
    ALAC = "alac"
    WAV = "wav"
    OPUS = "opus"
    FLAC = "flac"
    MKV = "mkv"
    JSON = "json"
    UNKNOWN = ""

    @staticmethod
    # Forward Reference used here in type hint
    def get_all() -> list[FileType]:
        return list(FileType)

    @staticmethod
    def get_file_type_from_str(file_type_candidate: str) -> FileType:
        file_types = FileType.get_all()
        file_type_candidate = file_type_candidate.lower()

        for file_type in file_types:
            if file_type_candidate == file_type.value.lower():
                return file_type

        raise ValueError("File Type not supported: " + file_type_candidate)

    @staticmethod
    def get_musical_file_type_from_str(file_type_candidate: str) -> FileType:
        file_type_candidate = file_type_candidate.lower()
        file_types = [
            FileType.MP3,
            FileType.MP4,
            FileType.AAC,
            FileType.OGG,
            FileType.WMA,
            FileType.ALAC,
            FileType.WAV,
            FileType.OPUS,
            FileType.FLAC,
        ]

        for file_type in file_types:
            if file_type_candidate == file_type.value.lower():
                return file_type

        raise ValueError("File Type not supported: " + file_type_candidate)
