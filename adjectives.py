from lemminflect import getLemma, getInflection

VOWELS = "aeiouy"
grade_irregular = {
    "hind": ("hinder", "hindmost"),
    "ill": ("worse", "worst"),
    "little": ("less", "least"),
    "many": ("more", "most")
}

grade_uninflected = ["giant", "glib", "hurt", "known", "madly"]

COMPARATIVE = "er"
SUPERLATIVE = "est"


def _count_syllables(word):
    """ Returns the estimated number of syllables in the word by counting vowel-groups.
    """
    n = 0
    p = False  # True if the previous character was a vowel.
    for ch in word.endswith("e") and word[:-1] or word:
        v = ch in VOWELS
        n += int(v and not p)
        p = v
    return n


def get_CorrectBase(lemma):
    return getLemma(lemma, 'ADJ')


def grade(adjective, suffix=COMPARATIVE, sentiment='positive'):
    """ Returns the comparative or superlative form of the given adjective.
    """
    tag = future_degree(suffix)
    adjective = adjective.text
    n = _count_syllables(adjective)
    length_adjective = len(adjective.split())
    is_irregular = any(lemmas in getLemma(adjective, 'ADJ') for lemmas in grade_irregular)
    is_irregular_list = [lemmas for lemmas in grade_irregular if lemmas in getLemma(adjective, 'ADJ')]
    if suffix == 'positive':
        return getLemma(adjective, 'ADJ')[0]
    elif is_irregular:
        # A number of adjectives inflect irregularly and aren't picked up correctly by
        if tag == 'JJR':
            return grade_irregular.get(is_irregular_list[0])[0]
        else:
            return grade_irregular.get(is_irregular_list[0])[1]
    elif adjective in grade_uninflected:
        # A number of adjectives don't inflect at all.
        if length_adjective == 1 and sentiment == 'positive':
            return "%s %s" % (suffix == COMPARATIVE and "more" or "most", adjective)
        elif length_adjective == 1 and sentiment == 'negative':
            return "%s %s" % (suffix == COMPARATIVE and "less" or "least", adjective)
        elif length_adjective == 2 and sentiment == 'positive':
            return "%s %s" % (suffix == COMPARATIVE and "more" or "most", adjective.split(' ')[1])
        else:
            return "%s %s" % (suffix == COMPARATIVE and "less" or "least", adjective.split(' ')[1])
    elif n == 1:
        return getInflection(getLemma(adjective, 'ADJ')[0], tag)[0]
    elif n <= 2 and adjective.endswith("e"):
        return getInflection(getLemma(adjective, 'ADJ')[0], tag)[0]
    elif n == 2 and adjective.endswith("y"):
        return getInflection(getLemma(adjective, 'ADJ')[0], tag)[0]
    elif n == 2 and adjective[-2:] in ("er", "le", "ow"):
        return getInflection(getLemma(adjective, 'ADJ')[0], tag)[0]
    else:
        # With three or more syllables: more generous, more important.
        if length_adjective == 1 and sentiment == 'positive':
            return "%s %s" % (suffix == COMPARATIVE and "more" or "most", adjective)
        elif length_adjective == 1 and sentiment == 'negative':
            return "%s %s" % (suffix == COMPARATIVE and "less" or "least", adjective)
        elif length_adjective == 2 and sentiment == 'positive':
            return "%s %s" % (suffix == COMPARATIVE and "more" or "most", adjective.split(' ')[1])
        else:
            return "%s %s" % (suffix == COMPARATIVE and "less" or "least", adjective.split(' ')[1])


def positive(adjective):
    return grade(adjective, suffix='positive')


def comparative(adjective, sentiment='positive'):
    return grade(adjective, COMPARATIVE, sentiment)


def superlative(adjective, sentiment='positive'):
    return grade(adjective, SUPERLATIVE, sentiment)


def determine_degree(adjective):
    adjective_length = len(adjective.text.split())
    if adjective_length == 1:
        return adjective.tag_
    else:
        return adjective[1].tag_


def future_degree(text):
    if text == COMPARATIVE:
        return "JJR"
    elif text == SUPERLATIVE:
        return "JJS"
    else:
        return 'positive'
