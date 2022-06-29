import spacy
import sentence_structure as sv

nlp = spacy.load("en_core_web_lg")


class Swaps:
    def __init__(self, docs, nlp=None):
        self.docs = docs
        self.nlp = nlp
        if not self.nlp:
            spacy.cli.download("en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg", disable=['lemmatizer'])

    def mass_sov(self):
        all_docs = []
        for doc in self.nlp.pipe(self.docs, batch_size=500):
            new_sent = ""
            for sent in [sent.as_doc() for sent in doc.sents]:
                nw = to_newwords(sent)
                triples = sv.get_triples(sent)
                svo_links = check_overlap(check_same_links(sv.svo_links(triples)))
                print(svo_links)
                if not svo_links:
                    new_sent = new_sent + sent.text_with_ws
                else:
                    new_sent = new_sent + make_new_text(to_sov(nw, svo_links))
            all_docs.append(new_sent)
        return all_docs

    def mass_vso(self):
        all_docs = []
        for doc in self.nlp.pipe(self.docs, batch_size=500):
            new_sent = ""
            for sent in [sent.as_doc() for sent in doc.sents]:
                nw = to_newwords(sent)
                triples = sv.get_triples(sent)
                svo_links = check_overlap(check_same_links(sv.svo_links(triples)))
                if not svo_links:
                    new_sent = new_sent + sent.text_with_ws
                else:
                    new_sent = new_sent + make_new_text(to_vso(nw, svo_links))
            all_docs.append(new_sent)
        return all_docs

    def mass_vos(self):
        all_docs = []
        for doc in self.nlp.pipe(self.docs, batch_size=500):
            new_sent = ""
            for sent in [sent.as_doc() for sent in doc.sents]:
                nw = to_newwords(sent)
                triples = sv.get_triples(sent)
                svo_links = check_overlap(check_same_links(sv.svo_links(triples)))
                if not svo_links:
                    new_sent = new_sent + sent.text_with_ws
                else:
                    new_sent = new_sent + make_new_text(to_vos(nw, svo_links))
            all_docs.append(new_sent)
        return all_docs

    def mass_osv(self):
        all_docs = []
        for doc in self.nlp.pipe(self.docs, batch_size=500):
            new_sent = ""
            for sent in [sent.as_doc() for sent in doc.sents]:
                nw = to_newwords(sent)
                triples = sv.get_triples(sent)
                svo_links = check_overlap(check_same_links(sv.svo_links(triples)))
                if not svo_links:
                    new_sent = new_sent + sent.text_with_ws
                else:
                    new_sent = new_sent + make_new_text(to_osv(nw, svo_links))
            all_docs.append(new_sent)
        return all_docs

    def mass_ovs(self):
        all_docs = []
        for doc in self.nlp.pipe(self.docs, batch_size=500):
            new_sent = ""
            for sent in [sent.as_doc() for sent in doc.sents]:
                nw = to_newwords(sent)
                triples = sv.get_triples(sent)
                svo_links = check_overlap(check_same_links(sv.svo_links(triples)))
                if not svo_links:
                    new_sent = new_sent + sent.text_with_ws
                else:
                    new_sent = new_sent + make_new_text(to_ovs(nw, svo_links))
            all_docs.append(new_sent)
        return all_docs


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


def to_sov(newwords, svo_links):
    newdoc = newwords[:]
    verb1 = [svo_link[1] for svo_link in svo_links]
    object1 = [svo_link[2] for svo_link in svo_links]
    for i in range(len(verb1)):
        newdoc[verb1[i].start] = NewWord(
            text=object1[i].text,
            ws=verb1[i][-1].whitespace_
        )
        newdoc[object1[i].start] = NewWord(
            text=verb1[i].text,
            ws=object1[i][-1].whitespace_
        )

    verbs_list = [newdoc[verb.start + 1: verb.end] for verb in verb1]
    objects_list = [newdoc[object.start + 1: object.end] for object in object1]
    for verbs in verbs_list:
        for slic in verbs:
            newdoc.remove(slic)
    for objects in objects_list:
        for slic2 in objects:
            newdoc.remove(slic2)
    return newdoc


def to_osv(newwords, svo_links):
    newdoc = newwords[:]
    for i in range(len(svo_links)):
        newdoc[svo_links[i][0].start] = NewWord(
            text=svo_links[i][2].text,
            ws=svo_links[i][0][-1].whitespace_
        )
        newdoc[svo_links[i][1].start] = NewWord(
            text=svo_links[i][0].text,
            ws=svo_links[i][1][-1].whitespace_
        )
        newdoc[svo_links[i][2].start] = NewWord(
            text=svo_links[i][1].text,
            ws=svo_links[i][2][-1].whitespace_
        )

    subjects_list = [newdoc[svo_link[0].start + 1: svo_link[0].end] for svo_link in svo_links]
    verbs_list = [newdoc[svo_link[1].start + 1: svo_link[1].end] for svo_link in svo_links]
    objects_list = [newdoc[svo_link[2].start + 1: svo_link[2].end] for svo_link in svo_links]
    for subjects in subjects_list:
        for slic in subjects:
            newdoc.remove(slic)
    for verbs in verbs_list:
        for slic2 in verbs:
            newdoc.remove(slic2)
    for objects in objects_list:
        for slic3 in objects:
            newdoc.remove(slic3)
    return newdoc


def to_vso(newwords, svo_links):
    newdoc = newwords[:]
    for i in range(len(svo_links)):
        newdoc[svo_links[i][0].start] = NewWord(
            text=svo_links[i][1].text,
            ws=svo_links[i][0][-1].whitespace_
        )
        newdoc[svo_links[i][1].start] = NewWord(
            text=svo_links[i][0].text,
            ws=svo_links[i][1][-1].whitespace_
        )

    subjects_list = [newdoc[svo_link[0].start + 1: svo_link[0].end] for svo_link in svo_links]
    verbs_list = [newdoc[svo_link[1].start + 1: svo_link[1].end] for svo_link in svo_links]
    for subjects in subjects_list:
        for slic in subjects:
            newdoc.remove(slic)
    for verbs in verbs_list:
        for slic2 in verbs:
            newdoc.remove(slic2)
    return newdoc


def to_vos(newwords, svo_links):
    newdoc = newwords[:]
    for i in range(len(svo_links)):
        newdoc[svo_links[i][0].start] = NewWord(
            text=svo_links[i][1].text,
            ws=svo_links[i][0][-1].whitespace_
        )
        newdoc[svo_links[i][1].start] = NewWord(
            text=svo_links[i][2].text,
            ws=svo_links[i][1][-1].whitespace_
        )
        newdoc[svo_links[i][2].start] = NewWord(
            text=svo_links[i][0].text,
            ws=svo_links[i][2][-1].whitespace_
        )

    subjects_list = [newdoc[svo_link[0].start + 1: svo_link[0].end] for svo_link in svo_links]
    verbs_list = [newdoc[svo_link[1].start + 1: svo_link[1].end] for svo_link in svo_links]
    objects_list = [newdoc[svo_link[2].start + 1: svo_link[2].end] for svo_link in svo_links]
    for subjects in subjects_list:
        for slic in subjects:
            newdoc.remove(slic)
    for verbs in verbs_list:
        for slic2 in verbs:
            newdoc.remove(slic2)
    for objects in objects_list:
        for slic3 in objects:
            newdoc.remove(slic3)
    return newdoc


def to_ovs(newwords, svo_links):
    newdoc = newwords[:]
    for i in range(len(svo_links)):
        newdoc[svo_links[i][0].start] = NewWord(
            text=svo_links[i][2].text,
            ws=svo_links[i][0][-1].whitespace_
        )
        newdoc[svo_links[i][2].start] = NewWord(
            text=svo_links[i][0].text,
            ws=svo_links[i][2][-1].whitespace_
        )

    subjects_list = [newdoc[svo_link[0].start + 1: svo_link[0].end] for svo_link in svo_links]
    objects_list = [newdoc[svo_link[2].start + 1: svo_link[2].end] for svo_link in svo_links]
    for subjects in subjects_list:
        for slic in subjects:
            newdoc.remove(slic)
    for objects in objects_list:
        for slic2 in objects:
            newdoc.remove(slic2)
    return newdoc


def check_same_links(svo_links):
    """
    Some svos are not svo, but are still linked. Remove those
    :return:
    """
    seen = set()
    return [(a, b, c) for a, b, c in svo_links if not (b in seen or seen.add(b))]


def check_overlap(svo_links):
    return [(a, b, c) for a, b, c in svo_links if (a.end <= b.start and b.end <= c.start)]


def make_new_text(new_words):
    return "".join(
        new_word.text + new_word.ws
        for new_word in new_words
    )
