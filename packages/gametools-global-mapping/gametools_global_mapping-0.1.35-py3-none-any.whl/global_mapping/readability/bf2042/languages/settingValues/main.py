from global_mapping.readability.bf2042.saved_items.singleton import Singleton
from . import (
    ar_sa,
    de_de,
    en_us,
    es_es,
    es_mx,
    fr_fr,
    it_it,
    ja_jp,
    ko_kr,
    pl_pl,
    ru_ru,
    zh_cn,
    zh_tw,
    pt_br,
)


class LangSwitch(metaclass=Singleton):
    __langs: dict = {
        "ar-sa": ar_sa.translation,
        "de-de": de_de.translation,
        "en-us": en_us.translation,
        "es-es": es_es.translation,
        "es-mx": es_mx.translation,
        "fr-fr": fr_fr.translation,
        "it-it": it_it.translation,
        "ja-jp": ja_jp.translation,
        "ko-kr": ko_kr.translation,
        "pl-pl": pl_pl.translation,
        "ru-ru": ru_ru.translation,
        "zh-cn": zh_cn.translation,
        "zh-tw": zh_tw.translation,
        "pt-br": pt_br.translation,
    }

    async def updateLanguage(self, lang: str, translation: dict):
        current_lang = self.__langs.get(f"{lang}", None)
        if current_lang is not None:
            self.__langs[lang] = translation

    async def get(self, lang: str):
        return self.__langs.get(f"{lang}".lower(), self.__langs["en-us"])


async def selectLanguage(lang: str):
    switcher = LangSwitch()
    return await switcher.get(lang)
