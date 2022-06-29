import spacy
import textacy
import textacy.resources
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import WordNetError
from nltk.stem import WordNetLemmatizer
import nltk
from textacy import utils as util_aug
from textacy.augmentation.transforms import _select_random_candidates
from textacy.augmentation.utils import to_aug_toks
from textacy.augmentation.utils import AugTok

wnl = WordNetLemmatizer()


class Definition:
    def __init__(self, docs, nlp=None):
        self.docs = docs
        self.nlp = nlp
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        rs = textacy.resources.ConceptNet()
        rs.download()
        if not self.nlp:
            spacy.cli.download("en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg")

    def mass_definition(self):
        return [make_new_text(self.definition_words(doc, ["NOUN", "VERB", "ADV", "ADJ"], 0.50))
                for doc in self.nlp.pipe(self.docs, batch_size=500)]

    def definition_words(self, doc, pos, num):
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
            text=decide_definition(aug_tok),
            ws=aug_tok.ws,
            pos=aug_tok.pos,
            is_word=aug_tok.is_word,
            syns=aug_tok.syns,
        )
                if idx in rand_idxs
                else aug_tok
                for idx, aug_tok, in enumerate(aug_toks)
                ]


def definition_words(doc, pos, num):
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
        text=decide_definition(aug_tok),
        ws=aug_tok.ws,
        pos=aug_tok.pos,
        is_word=aug_tok.is_word,
        syns=aug_tok.syns,
    )
            if idx in rand_idxs
            else aug_tok
            for idx, aug_tok, in enumerate(aug_toks)
            ]


def make_new_spacy_doc(aug_toks):
    new_text = "".join(
        aug_tok.text + aug_tok.ws
        for aug_tok in aug_toks
    )
    return textacy.spacier.core.make_spacy_doc(new_text, "en_core_web_lg")


def make_new_text(aug_toks):
    return "".join(
        aug_tok.text + aug_tok.ws
        for aug_tok in aug_toks
    )


def decide_definition(aug_tok):
    pos_dict = {'NOUN': 'n',
                'VERB': 'v',
                'ADJ': 'a',
                'ADV': 'r'}
    try:
        return wn.synset(wnl.lemmatize(aug_tok.text, pos=pos_dict.get(aug_tok.pos)) + "." + pos_dict.get(
        aug_tok.pos) + '.01').definition()
    except WordNetError:
        return aug_tok.text

#if __name__ == "__main__":
#    main()
