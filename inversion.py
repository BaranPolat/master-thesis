from textacy import extract
import spacy
from datasets import load_dataset

pattern = [{"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": "AUX"}, {"POS": "VERB"}]


class Inversion:
    def __init__(self, docs, nlp=None):
        self.docs = docs
        self.nlp = nlp
        if not self.nlp:
            spacy.cli.download("en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg")
            self.nlp.add_pipe('merge_noun_chunks')

    def mass_inversion(self):
        all_docs = []
        for doc in self.nlp.pipe(self.docs, batch_size=500):
            new_text = ""
            for sent in [sent.as_doc() for sent in doc.sents]:
                inverses = list(extract.token_matches(sent, patterns=pattern))
                newdoc = to_newwords(sent)
                if len(inverses) < 1:
                    new_text = new_text + sent.text
               #     print(new_text)
                else:
                    verbs = [inverse for inverse in inverses]
                    for verb in verbs:
                        newdoc = put_aux_in_front(sent, newdoc, verb)
                    new_text = new_text + make_new_text(newdoc)
            all_docs.append(new_text)
        return all_docs


class NewWord:
    def __init__(self, text, ws):
        self.text = text
        self.ws = ws


def to_newwords(doc):
    newwords_list = []
    for token in doc:
        newwords_list.append(NewWord(text=token.text, ws=token.whitespace_))
    return newwords_list


def put_aux_in_front(sentence, newwords, pattern):
    nw = newwords[:]
    nw[-1] = NewWord("?", nw[-1].ws)
    ents = [str(ent) for ent in sentence.ents]
    if not pattern:
        return newwords
    if pattern.start == 0:
        nw.insert(pattern.start, NewWord(pattern[-2].text.capitalize(), " "))
        del nw[pattern[-2].i + 1]
        if any(pattern[0:-2].text in ent for ent in ents):
            return nw
        else:
            nw[1] = NewWord(nw[1].text.lower(), nw[1].ws)
            return nw
    nw.insert(pattern.start, NewWord(pattern[-2].text, pattern[-2].whitespace_))
    del nw[pattern[-2].i + 1]
    return nw


def make_new_text(new_words):
    return "".join(
        new_word.text + new_word.ws
        for new_word in new_words
    )