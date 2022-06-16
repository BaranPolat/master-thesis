from lemminflect import getLemma, getInflection

VOWELS = "aeiouy"
grade_irregular = {
    "bad": ("worse", "worst"),
    "far": ("further", "farthest"),
    "good": ("better", "best"),
    "hind": ("hinder", "hindmost"),
    "ill": ("worse", "worst"),
    "less": ("lesser", "least"),
    "little": ("less", "least"),
    "many": ("more", "most"),
    "much": ("more", "most"),
    "well": ("better", "best")
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


def grade(adjective, suffix=COMPARATIVE, sentiment='positive'):
    """ Returns the comparative or superlative form of the given adjective.
    """
    adjective = adjective.text
    n = _count_syllables(adjective)
    length_adjective = len(adjective.split())
    is_irregular = any(lemmas in getLemma(adjective, 'ADJ') for lemmas in grade_irregular)
    if suffix == 'positive':
        return getLemma(adjective, 'ADJ')
    elif is_irregular:
        # A number of adjectives inflect irregularly.
        if suffix == COMPARATIVE:
            return getInflection(getLemma(adjective, 'ADJ')[0], 'JJR')
        if suffix == SUPERLATIVE:
            return getInflection(getLemma(adjective, 'ADJ')[0], 'JJS')
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
    elif n <= 2 and adjective.endswith("e"):
        # With one syllable and ending with an e: larger, wiser.
        suffix = suffix.lstrip("e")
    elif n == 1 and len(adjective) >= 3 \
            and adjective[-1] not in VOWELS and adjective[-2] in VOWELS and adjective[-3] not in VOWELS:
        # With one syllable ending with consonant-vowel-consonant: bigger, thinner.
        if not adjective.endswith("w"):  # Exceptions: lower, newer.
            suffix = adjective[-1] + suffix
    elif n == 1:
        # With one syllable ending with more consonants or vowels: briefer.
        pass
    elif n == 2 and adjective.endswith("y"):
        # With two syllables ending with a y: funnier, hairier.
        adjective = adjective[:-1] + "i"
    elif n == 2 and adjective[-2:] in ("er", "le", "ow"):
        # With two syllables and specific suffixes: gentler, narrower.
        pass
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
    return adjective + suffix


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
