import random
import spacy
import textacy
from spacy.util import filter_spans
from textacy import extract

random.seed(420)
OBJECTS = {"pobj", "dobj", "dative", "attr", "oprd"}
SUBJECTS = {"nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"}
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('merge_noun_chunks')
text = 'He is a bad person, but the better player. But, as long as he scores points, they should shut up. Was John in New York? In the end, it doesnt even matter for Johan'
vp_patterns = [
    [
        {"POS": {"IN": ["ADV", "AUX", "PART", "VERB"]}, "OP": "*"},
        {"POS": {"IN": ["AUX", "VERB"]}},
    ]
]
doc = nlp(text)


# for token in doc:
#    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#        token.shape_, token.is_alpha, token.is_stop)


def main():
    sentences = [i for i in nlp(text).sents]
    for i in sentences:
        print(i)
        triples = get_triples(i)
        svo_link_lists = svo_links(triples)
        print(svo_link_lists)
        if not svo_link_lists:
            print(sv_links(triples))


#    doc2 = nlp("But, as long as he scores points, they should shut up.")
#    for token in doc2:
#        print(token.text, token.pos_, token.tag_, token.dep_, token.head)


def pos_switcher(doc, pos):
    noun_list = [token for token in doc if token.pos_ == pos]
    i_list = [noun.i for noun in noun_list]
    new_sentence = ""
    for token in doc:
        if token.i in i_list:
            excl_n = token.i
            sample_list = [number for number in i_list if number != excl_n]
            random_number = random.choice(sample_list)
            new_sentence = new_sentence + doc[random_number].text_with_ws
        else:
            new_sentence = new_sentence + token.text_with_ws
    return new_sentence


def identify_verbs(doc):
    verb_phrases = textacy.extract.token_matches(doc, patterns=vp_patterns)
    vp_list = [verb_phrase for verb_phrase in verb_phrases]
    filtered = filter_spans(vp_list)
    return filtered


def identify_objects(doc):
    chunks = doc.noun_chunks
    return [chunk for chunk in chunks for word in chunk if word.dep_ in OBJECTS]


def identify_subjects(doc):
    chunks = doc.noun_chunks
    return [chunk for chunk in chunks for word in chunk if word.dep_ in SUBJECTS]


def get_triples(doc):
    objects = identify_objects(doc)
    subjects = identify_subjects(doc)
    verbs = identify_verbs(doc)
    return {"subjects": subjects, "verbs": verbs, "objects": objects}


def get_heads(doc):
    heads = [token.head for token in doc]
    return heads


def sv_links(svo):
    subjects = svo.get('subjects')
    verbs = svo.get('verbs')
    lists = [
        (subject, vp)
        for subject in subjects
        for word in subject
        for vp in verbs
        if word.head in vp
    ]
    return lists


def get_closest_verb(noun_chunk, vp):
    if noun_chunk.head in vp:
        return True
    elif noun_chunk.head.pos_ == 'ADP':
        if noun_chunk.head.head in vp:
            return True
    else:
        return False


def check_svo_structure(subject, vp, object):
    return subject.start < vp.start < object.start


def object_position_verifier(noun_chunk, vp):
    return noun_chunk.start >= vp.end


def svo_links(svo):
    subjects = svo.get('subjects')
    verbs = svo.get('verbs')
    objects = svo.get('objects')
    lists = [
        (subject, vp, object)
        for vp in verbs
        for subject in subjects
        for word in subject
        for object in objects
        for word2 in object
        if all([get_closest_verb(word, vp), get_closest_verb(word2, vp)])
        # if all([word.head in vp, word2.head in vp])
    ]
    return lists


if __name__ == "__main__":
    main()
