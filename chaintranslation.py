import random
from itertools import combinations

import googletrans
import spacy
from googletrans import Translator
import httpx

random.seed(10)


def random_languages(all_languages, amount):
    return [random.choice(list(all_languages)) for i in range(amount)]


class ChainTranslation:

    def __init__(self, doc):
        self.doc = doc
        self.translated = ""

    def chain_translate(self, src_lang, languages=random_languages(googletrans.LANGUAGES, 1)):
        return chaintranslation(self.doc, src_lang, languages)


def chaintranslation(text, source_language, languages=random_languages(googletrans.LANGUAGES, 1)):
    translator = Translator(timeout=httpx.Timeout(5))
    translated = text
    src = source_language
    for language in languages:
        translated = translator.translate(translated, dest=language, src=src).text
        print(translated)
        src = language
    translated = translator.translate(translated, dest=source_language, src=src)
    return translated.text

def mass_chaintranslation(texts, source_language, languages=random_languages(googletrans.LANGUAGES, 1)):
    translator = Translator(timeout=httpx.Timeout(10))
    translated = texts
    src = source_language
    for language in languages:
        translated = [translator.text for translator in translator.translate(translated, dest=language, src=src)]
        src = language
    translated = [translator.text for translator in translator.translate(translated, dest=source_language, src=src)]
    return translated


def create_combinations(languages, length):
    return combinations(languages, length)