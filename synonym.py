import random
import operator
import spacy
import textacy
import textacy.resources
# from textacy.types import AugTok
from textacy import utils as util_aug
from textacy.augmentation.transforms import _select_random_candidates
from textacy.augmentation.utils import to_aug_toks
from textacy.augmentation.utils import AugTok

from textacy import preprocessing
from nltk.corpus import wordnet

# ------------------------------------------------------------------------------------------------------------------------


rs = textacy.resources.ConceptNet()
rs.download()


class Synonym:
    def __init__(self, docs, nlp=None):
        self.docs = docs
        self.nlp = nlp
        rs = textacy.resources.ConceptNet()
        rs.download()
        if not self.nlp:
            spacy.cli.download("en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg")

    def mass_synonyms(self):
        return [make_new_text(self.synonym_words(doc, ["NOUN", "VERB", "ADV", "ADJ"], 0.25))
                for doc in self.nlp.pipe(self.docs, batch_size=500)]

    def synonym_words(self, doc, pos, num):
        aug_toks = to_aug_toks(doc)
        pos = util_aug.to_collection(pos, str, set)
        cand_idxs = [
            idx
            for idx, aug_tok in enumerate(aug_toks)
            if aug_tok.syns and (pos is None or aug_tok.pos in pos)
        ]
        rand_idxs = set(_select_random_candidates(cand_idxs, num))
        if not rand_idxs:
            return aug_toks[:]

        return [AugTok(
            # text=random.choice(decide_synonyms(aug_tok)),  reason: for synonyms but with whitespace priority
            # text=max(decide_synonyms_vec(aug_tok, self.nlp), key=operator.itemgetter(1))[0], reason: for synonyms with whitespace priority and highest vector
            text=max(decide_synonyms_nowhitespace(aug_tok, self.nlp), key=operator.itemgetter(1))[0],
            ws=aug_tok.ws,
            pos=aug_tok.pos,
            is_word=aug_tok.is_word,
            syns=aug_tok.syns,
        )
                if idx in rand_idxs
                else aug_tok
                for idx, aug_tok, in enumerate(aug_toks)
                ]


"""
        new_aug_toks = []
        
        
        for idx, aug_tok, in enumerate(aug_toks):
            if idx in rand_idxs:
                new_aug_toks.append(
                    AugTok(
                        text=random.choice(decide_synonyms(aug_tok)),
                        ws=aug_tok.ws,
                        pos=aug_tok.pos,
                        is_word=aug_tok.is_word,
                        syns=aug_tok.syns,
                    )
                )
            else:
                new_aug_toks.append(aug_tok)
"""


#  return new_aug_toks


def make_new_spacy_doc(aug_toks):
    new_text = "".join(
        aug_tok.text + aug_tok.ws
        for aug_tok in aug_toks
    )
    return textacy.spacier.core.make_spacy_doc(new_text, "en_core_web_sm")


def make_new_text(aug_toks):
    return "".join(
        aug_tok.text + aug_tok.ws
        for aug_tok in aug_toks
    )


def decide_synonyms(aug_tok):
    if any(' ' in syn for syn in aug_tok.syns):
        return [syn
                for syn in aug_tok.syns
                if ' ' in syn]
    else:
        return aug_tok.syns


def decide_synonyms_vec(aug_tok, nlp):
    if any(' ' in syn for syn in aug_tok.syns):
        synset = [syn
                  for syn in aug_tok.syns
                  if ' ' in syn]
        return [(syn, nlp(aug_tok.text).similarity(nlp(syn))) for syn in synset]
    else:
        return [(syn, nlp(aug_tok.text).similarity(nlp(syn))) for syn in aug_tok.syns]


def decide_synonyms_nowhitespace(aug_tok, nlp):
    return [(syn, nlp(aug_tok.text).similarity(nlp(syn))) for syn in aug_tok.syns]

# nlp = spacy.load("en_core_web_lg")

# syno = Synonym([nlp("Home is where the heart is")], nlp)
# print(syno.mass_synonyms())

# https://www.geeksforgeeks.org/nlp-synsets-for-a-word-in-wordnet/
# https://github.com/recognai/spacy-wordnet/blob/master/spacy_wordnet/wordnet_domains.py
