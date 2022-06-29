import spacy
import random
import adjectives as adj_test

class PeriPhrasis:
    def __init__(self, docs, nlp=None):
        self.docs = docs
        self.nlp = nlp
        if not self.nlp:
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm", disable=["ner", "parser", "lemmatizer"])

    def mass_adjectives(self):
        all_docs = []
        for doc in self.nlp.pipe(self.docs, batch_size=500):
            adjectives = find_adjectives(doc)
            new_adjectives = []
            for adjective in adjectives:
                coin_toss = random.randint(0, 1)
                if(type(adjective)==spacy.tokens.span.Span):
                    start = adjective.start
                else:
                    start = adjective.i
                if adj_test.determine_degree(adjective) == 'JJ':
                    if coin_toss == 0:
                        new_adjectives.append((adj_test.comparative(adjective), start))
                    else:
                        new_adjectives.append((adj_test.superlative(adjective), start))
                elif adj_test.determine_degree(adjective) == 'JJR':
                    if coin_toss == 0:
                        new_adjectives.append((adj_test.positive(adjective), start))
                    else:
                        new_adjectives.append((adj_test.superlative(adjective), start))
                else:
                    if coin_toss == 0:
                        new_adjectives.append((adj_test.positive(adjective), start))
                    else:
                        new_adjectives.append((adj_test.comparative(adjective), start))
            newdoc = ""
            start_point = 0
            for new_adjective in new_adjectives:
                newdoc = newdoc + doc[start_point:new_adjective[1]].text_with_ws + new_adjective[0] + doc[new_adjective[1]].whitespace_
                start_point = new_adjective[1] + 1
            newdoc = newdoc + doc[start_point:].text
            all_docs.append(newdoc)
        return all_docs


def find_adjectives(doc):
    adjective_list = []
    for i, token in enumerate(doc):
        if (i + 1 < len(doc)):
            adverb = (token.tag_ == 'RBR' or token.tag_ == 'RBS')
            adjective = doc[i + 1].pos_ == 'ADJ'
            if (adverb and adjective):
                adjective_list.append(doc[i:i + 2])
            elif (not adverb and adjective):
                adjective_list.append(doc[i + 1])
    return adjective_list