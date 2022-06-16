import spacy
import sentence_structure as sv
import itertools
from datasets import load_dataset

nlp = spacy.load("en_core_web_lg")
text1 = nlp(
    'He is a bad person, but the better player. But, as long as he scores points, they should shut up. Was John in New York? In the end, it doesnt even matter for Johan')
text2 = nlp('He is not a bad person, but the better player.')
text3 = nlp("In the end, it doesnt even matter for Johan.")


def main():
    """
    sents = [sent.as_doc() for sent in text1.sents]
    for sent in sents:
        nw = to_newwords(sent)
        triples = sv.get_triples(sent)
        svo_links = sv.svo_links(triples)
#        print(svo_links)
        for svo_link in svo_links:
#            print(svo_link)
            sooo = to_sov(nw, svo_link)
#            print(make_new_text(sooo))
    """
    raw_dataset = load_dataset('xsum')
    datas=nlp(raw_dataset["train"][203000]['document'])
    sents=[sent.as_doc() for sent in datas.sents]
    for sent in sents:
        nw=to_newwords(sent)
        triples = sv.get_triples(sent)
        svo_links = sv.svo_links(triples)
        print(svo_links)
        for svo_link in svo_links:
            print(svo_link)
            sooo = to_sov(nw, svo_link)
            print(make_new_text(sooo))

class NewWord:
    def __init__(self, text, ws):
        self.text = text
        self.ws = ws
        # https://textacy.readthedocs.io/en/latest/_modules/textacy/augmentation/transforms.html#swap_words


def to_newwords(doc):
    newwords_list = []
    for token in doc:
        newwords_list.append(NewWord(text=token.text, ws=token.whitespace_))
    return newwords_list


def to_sov(newwords, svo_link):
    newdoc = newwords[:]
    print("Original: ", make_new_text(newdoc))
    verb1 = svo_link[1]
    object1 = svo_link[2]
    newdoc[verb1.start] = NewWord(
        text=object1.text,
        ws=verb1[-1].whitespace_
    )
    newdoc[object1.start] = NewWord(
        text=verb1.text,
        ws=object1[-1].whitespace_
    )
    verbs_list = newdoc[verb1.start+1 : verb1.end]
    objects_list = newdoc[object1.start+1 : object1.end]
    for slic in verbs_list:
        newdoc.remove(slic)
    for slic2 in objects_list:
        newdoc.remove(slic2)
    return newdoc


def make_new_text(new_words):
    return "".join(
        new_word.text + new_word.ws
        for new_word in new_words
    )


def check_same_links(svo_link):
    """
    Some svos are not svo, but are still linked. Remove those
    :return:
    """
    subjects = [s[0] for s in svo_link]
    verbs = [v[1] for v in svo_link]
    objects = [o[1] for o in svo_link]
    for a, b in itertools.combinations(subjects, 2):
        if a.start == b.start:
            return True
        else:
            continue
    for c, d in itertools.combinations(verbs, 2):
        if c.start == d.start:
            return True
        else:
            continue
    for e, f in itertools.combinations(objects, 2):
        if e.start == f.start:
            return True
        else:
            continue
    return False





if __name__ == "__main__":
    main()
