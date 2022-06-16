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

#print(googletrans.LANGUAGES)
print(chaintranslation("As long as he scores, they should shut up", "en", ['tr', 'de']))
#language_combinations = list(pickle.load(open("LanguageCombinations/LanguageCombinations_2.p", "rb")))
#line73 path = r"C:\Users\Baran\Documents\Huiswerk\Master\Thesis\Code\output.xlsx"
"""
original_length = len(doc.text.split())
original_split = doc.text.split()
all_values = []
doctext = doc.text

for language_combo in language_combinations:
    translated = chaintranslation(doc, "en", language_combo)
    new_length = len(translated.split())
    difference = abs(original_length - new_length)
    count = Counter(original_split) - Counter(translated.split())
    unique = sum({x: count for x, count in count.items() if count < 2}.values())
    all_values.append({'Languages': language_combo,
                                     'Original text': doctext,
                                     'New text': translated,
                                     'Difference': difference,
                                     'Unique words': unique
    })
df = pd.DataFrame(all_values)


book = load_workbook(path)
writer = pd.ExcelWriter(path, engine='openpyxl')
writer.book = book

df.to_excel(writer, index=False, sheet_name = "results2")
writer.save()

"""