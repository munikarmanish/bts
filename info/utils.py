import string

import numpy as n
from bugs.models import BugCategory, BugReport
from django.db.models import Count
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from .models import Frequency, FrequencyDetail, FrequencyTitle


def tokenize(text):
    """Returns a list of stemmed and stopwords-removed tokens of the
    given text.

    Parameters
    ----------
    text : string
        The text to tokenize
    """
    lowers = text.lower()
    punct_free = lowers.translate(str.maketrans({key: None for key in string.punctuation}))
    tokens = word_tokenize(punct_free)
    porter = PorterStemmer()
    stemmed = [porter.stem(w) for w in tokens]
    tokens = [w for w in stemmed if w not in stopwords.words('english')]
    return tokens


# The term frequencies (TF)

def tf(bug, term):
    """Return the term frequency of a term in a bug report.
    This is based on both title and description fields.
    """
    qs = Frequency.objects.filter(bug=bug, term=term)
    if qs.count() > 0:
        return qs.first().freq
    else:
        return 0


def tf_title(bug, term):
    """Return the term frequency of a term in a bug report.
    This is based on title field.
    """
    qs = FrequencyTitle.objects.filter(bug=bug, term=term)
    if qs.count() > 0:
        return qs.first().freq
    else:
        return 0


def tf_detail(bug, term):
    """Return the term frequency of a term in a bug report.
    This is based on description field.
    """
    qs = FrequencyDetail.objects.filter(bug=bug, term=term)
    if qs.count() > 0:
        return qs.first().freq
    else:
        return 0


# The inverse document frequencies (IDF)

def idf(term):
    """Returns the IDF of a term based on title + description.
    """
    Da = BugReport.objects.count()
    Dt = Frequency.objects.filter(term=term).count()
    return n.log2(Da / (1 + Dt))


def idf_title(term):
    """Returns the IDF of a term based on title.
    """
    Da = BugReport.objects.count()
    Dt = FrequencyTitle.objects.filter(term=term).count()
    return n.log2(Da / (1 + Dt))


def idf_detail(term):
    """Returns the IDF of a term based on description.
    """
    Da = BugReport.objects.count()
    Dt = FrequencyDetail.objects.filter(term=term).count()
    return n.log2(Da / (1 + Dt))


# The similarities

def similarity(text1, text2, idf_func=idf):
    """Returns the similarity between text1 and text2 based on the
    given IDF function.

    Parameters
    ----------
    text1, text2 : string
        Strings to calculate similarity between
    idf_func = \{idf, idf_title, idf_detail\}
        The IDF function to use for calculating similarity
    """
    common = set(tokenize(text1)).intersection(set(tokenize(text2)))
    return n.sum([idf_func(w) for w in common])


def feature_set(bug1, bug2):
    """Returns a list of (n-1) features for a pair of bug reports.
    """
    row = []
    for idf_func in [idf_title, idf_detail, idf]:
        for text1 in [bug1.title, bug1.detail_text(), bug1.all_text()]:
            for text2 in [bug2.title, bug2.detail_text(), bug2.all_text()]:
                row.append(similarity(text1, text2, idf_func))
    return row
