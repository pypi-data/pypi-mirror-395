from __future__ import annotations

from dataclasses import dataclass, field

from plexutil.enums.language import Language


# Frozen=True creates an implicit hash method, eq is created by default
@dataclass(frozen=True)
class TVLanguageManifestDTO:
    language: Language = Language.ENGLISH_US
    ids: list[int] = field(default_factory=list)
