from __future__ import annotations

from enum import Enum


class Language(Enum):
    ENGLISH_US = "en-US"
    ENGLISH_AUSTRALIA = "en-AU"
    ENGLISH_CANADA = "en-CA"
    ENGLISH_UK = "en-GB"
    SPANISH_SPAIN = "es-ES"
    SPANISH_MEXICO = "es-MX"
    ARABIC_SAUDI_ARABIA = "ar-SA"
    BULGARIAN = "bg-BG"
    CATALAN = "ca-ES"
    CHINESE = "zh-CN"
    CHINESE_HONG_KONG = "zh-HK"
    CHINESE_TAIWAN = "zh-TW"
    CROATIAN = "hr-HR"
    CZECH = "cs-CZ"
    DANISH = "da-DK"
    DUTCH = "nl-NL"
    ESTONIAN = "et-EE"
    FINNISH = "fi-FI"
    FRENCH = "fr-FR"
    FRENCH_CANADA = "fr-CA"
    GERMAN = "de-DE"
    GREEK = "el-GR"
    HEBREW = "he-IL"
    HINDI = "hi-IN"
    HUNGARIAN = "hu-HU"
    INDONESIAN = "id-ID"
    ITALIAN = "it-IT"
    JAPANESE = "ja-JP"
    KOREAN = "ko-KR"
    LATVIAN = "lv-LV"
    LITHUANIAN = "lt-LT"
    NORWEGIAN_BOKMAL = "nb-NO"
    PERSIAN = "fa-IR"
    POLISH = "pl-PL"
    PORTUGUESE = "pt-BR"
    PORTUGUESE_PORTUGAL = "pt-PT"
    ROMANIAN = "ro-RO"
    RUSSIAN = "ru-RU"
    SLOVAK = "sk-SK"
    SWEDISH = "sv-SE"
    THAI = "th-TH"
    TURKISH = "tr-TR"
    UKRAINIAN = "uk-UA"
    VIETNAMESE = "vi-VN"

    @staticmethod
    # Forward Reference used here in type hint
    def get_all() -> list[Language]:
        return list(Language)

    @staticmethod
    def get_from_str(candidate: str) -> Language:
        languages = Language.get_all()

        for language in languages:
            if candidate.lower() == language.value.lower():
                return language

        description = f"Language not supported: {candidate}"
        raise ValueError(description)
