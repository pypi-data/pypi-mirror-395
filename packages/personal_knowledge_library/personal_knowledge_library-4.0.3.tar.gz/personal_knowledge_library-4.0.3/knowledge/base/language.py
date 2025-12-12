# -*- coding: utf-8 -*-
# Copyright © 2024-present Wacom. All rights reserved.
from typing import NewType, List, Dict

#  ---------------------------------------- Type definitions -----------------------------------------------------------
LanguageCode = NewType("LanguageCode", str)
LocaleCode = NewType("LocaleCode", str)
# ------------------------------------------------ Language codes ------------------------------------------------------
EN_US: LocaleCode = LocaleCode("en_US")
JA_JP: LocaleCode = LocaleCode("ja_JP")
DE_DE: LocaleCode = LocaleCode("de_DE")
BG_BG: LocaleCode = LocaleCode("bg_BG")
FR_FR: LocaleCode = LocaleCode("fr_FR")
IT_IT: LocaleCode = LocaleCode("it_IT")
ES_ES: LocaleCode = LocaleCode("es_ES")
EN: LanguageCode = LanguageCode("en")
DE: LanguageCode = LanguageCode("de")
BG: LanguageCode = LanguageCode("bg")
JA: LanguageCode = LanguageCode("ja")
FR: LanguageCode = LanguageCode("fr")
IT: LanguageCode = LanguageCode("it")
ES: LanguageCode = LanguageCode("es")
# ----------------------------------------------------------------------------------------------------------------------
SUPPORTED_LOCALES: List[LocaleCode] = [JA_JP, EN_US, DE_DE, BG_BG, IT_IT]
SUPPORTED_LANGUAGES: List[LanguageCode] = [JA, EN, DE, BG, IT]
LANGUAGE_LOCALE_MAPPING: Dict[LanguageCode, LocaleCode] = dict(list(zip(SUPPORTED_LANGUAGES, SUPPORTED_LOCALES)))
LOCALE_LANGUAGE_MAPPING: Dict[LocaleCode, LanguageCode] = dict(list(zip(SUPPORTED_LOCALES, SUPPORTED_LANGUAGES)))
