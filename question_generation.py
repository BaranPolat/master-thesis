#import gensim.downloader as api
#wv = api.load('word2vec-google-news-300')
#print(wv.most_similar(positive=['new york'], topn=5))
from textacy import extract
import spacy
from spacy.util import filter_spans

pattern = [{"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": "AUX"}, {"POS": "VERB"}]
nlp = spacy.load("en_core_web_sm", disable=["ner"])
nlp.add_pipe('merge_noun_chunks')
doc = nlp('Pablo Picasso is working at the factory.')
doc = nlp("The fire alarm went off at the Holiday Inn in Hope Street at about 04:20 BST on Saturday and guest was asked to leave the hotel. As they gathered outside they saw the two buses, parked side-by-side in the car park, engulfed by flames. One of the tour groups is from Germany, the other from China and Taiwan. It was their first night in Northern Ireland. The driver of one of the buses said many of the passengers had left personal belongings on board and these had been destroyed. Both groups have organised replacement coaches and will begin their tour of the north coast later than they had planned. Polouse has appealed for information about the attack.")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.head)

questions = extract.token_matches(doc, patterns=pattern)
vp_list = [question for question in questions]
punctuations = [token for token in doc if token.text == "." and token.is_punct]
print(punctuations)
print(vp_list)
new_sentence = ""
for vp in vp_list:
    period = punctuations.pop(0)
    starting_point = 0
    if(vp.start_char == 0):
        print(vp.start_char, vp.end_char, vp.text_with_ws)
        new_sentence = new_sentence + vp[1].text_with_ws[0].capitalize() + vp[1].text_with_ws[1:] + vp[0].text_with_ws +\
                       vp[2].text_with_ws + doc[3:-1].text_with_ws + "?"
    else:
        new_sentence = new_sentence + doc.text[starting_point:vp.start_char] + vp[1].text_with_ws + \
                       vp[0].text_with_ws + vp[2].text_with_ws + doc[vp[2].i:period.i].text_with_ws + "?"
        #new_sentence = new_sentence + doc.text[:vp.start_char] + vp[1].text_with_ws[0] + vp[1].text_with_ws[1:] + vp[0].text_with_ws + \
        #               vp[2].text_with_ws + doc[3:-1].text_with_ws + "?"
print(new_sentence)
# Question generation = als auxillary verb en main verb in zitten, en dan in volgorde -> auxillary + subject + main verb
