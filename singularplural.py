import pattern
import spacy
import re
from pattern.text.en import INFINITIVE, PRESENT, PAST  # All tense forms
from pattern.text.en import SINGULAR, PLURAL  # For verb person
from pattern.text.en import singularize, pluralize  # For Nouns
import sentence_structure as sv

VERBS = ['MD', 'AUX', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
VERBS_PRESENT = ['VBP', 'VBZ', 'VBG']
VERBS_PAST = ['VBD', 'VBN']
VERB_MODAL = 'MD'
VERB_GERUND = 'VBG'
NOUNS = ['NN', 'NNS']
NOUNS_SINGULAR = ['NN']
NOUNS_PLURAL = ['NNS']
determiners = ['A', 'An', 'a', 'an']


# ASPECTS = [PROGRESSIVE, "perfective", "imperfective"]


class SingularPlural:
    def __init__(self, docs, nlp=None):
        self.docs = docs
        self.nlp = nlp
        if not self.nlp:
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])
            self.nlp.add_pipe('merge_noun_chunks')

    def sing_plur(self):
        pattern_stopiteration_workaround()
        all_docs = []
        for doc in self.nlp.pipe(self.docs, batch_size=500):
            triples = sv.get_triples(doc)
            sv_link = sv.sv_links(triples)
            singularized_pluralized = [siplu for sinplu in singularize_pluralize(doc, sv_link) for siplu in sinplu]
            newdoc = ""
            start_point = 0
            for singplur in singularized_pluralized:
                newdoc = newdoc + doc.text[start_point:singplur[1]] + singplur[0]
                start_point = singplur[2]
            newdoc = newdoc + doc.text[start_point:]
            all_docs.append(newdoc)
        return all_docs


def pattern_stopiteration_workaround():
    try:
        print(pattern.text.en.verbs.conjugate("come", PRESENT, 3, SINGULAR))
    except:
        pass


def filter_nouns(sv_link):
    determiner_patterns = re.compile(r'(\b[aA]n{0,1}\b)')
    return [link for link in sv_link for trip in link if trip[0].tag_ in NOUNS and not determiner_patterns.search(trip[0].text)]


def singularize_pluralize(doc, sv_link):
    filtered = filter_nouns(sv_link)
    new_list = []
    for word in filtered:
        if decide_number(word[0][0]) == PLURAL:
            new_list.append(((singularize(word[0].text), word[0].start_char, word[0].end_char),
                             (convert_verbs(word[1], SINGULAR), word[1].start_char, word[1].end_char)))
        else:
            new_list.append(((pluralize(word[0].text), word[0].start_char, word[0].end_char),
                             (convert_verbs(word[1], PLURAL), word[1].start_char, word[1].end_char)))
    return new_list


def convert_verbs(words, number):
    verb = ""
    if len(words) == 1:
        if words[0].tag_ == VERB_GERUND:
            pattern.text.en.verbs.conjugate(words[0].text, number=number, aspect='progressive')
        else:
            pattern.text.en.verbs.conjugate(words[0].text, number=number, tense=decide_tense(words[0]))
        return pattern.text.en.verbs.conjugate(words[0].text, number=number, tense=decide_tense(words[0]))
    else:
        for word in words:
            if word.tag_ == VERB_GERUND:
                verb = verb + " " + pattern.text.en.verbs.conjugate(word.text, number=number, aspect='progressive')
            elif word.tag_ == VERB_MODAL:
                verb = verb + " " + word.text
            else:
                verb = verb + " " + pattern.text.en.verbs.conjugate(word.text, number=number, tense=decide_tense(word))
        return verb[1:]


def decide_number(noun_phrase):
    if noun_phrase.tag_ in NOUNS_SINGULAR:
        return SINGULAR
    else:
        return PLURAL


def decide_tense(word):
    if word.tag_ in VERBS_PRESENT:
        return PRESENT
    elif word.tag_ in VERBS_PAST:
        return PAST
    else:
        return INFINITIVE


def replace_words(matcher, original_text, replacement):
    tok = original_text
    text = ''
    buffer_start = 0
    for _, match_start, _ in matcher(tok):
        if match_start > buffer_start:
            text += tok[buffer_start: match_start].text + tok[match_start - 1].whitespace_
        text += replacement + tok[match_start].whitespace_
        buffer_start = match_start + 1
    if buffer_start < len(tok):
        text += tok[buffer_start:].text
    return text