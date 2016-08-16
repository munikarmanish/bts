import string

import numpy as n
from bugs.models import BugCategory, BugReport
from django.db.models import Count
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from .models import Frequency, FrequencyDetail, FrequencyTitle


def tokenize(text):
    lowers = text.lower()
    punct_free = lowers.translate(str.maketrans({key: None for key in string.punctuation}))
    tokens = word_tokenize(punct_free)
    porter = PorterStemmer()
    stemmed = [porter.stem(w) for w in tokens]
    tokens = [w for w in stemmed if w not in stopwords.words('english')]
    return tokens


# The TFs

def tf(bug, term):
    qs = Frequency.objects.filter(bug=bug, term=term)
    if qs.count() > 0:
        return qs.first().freq
    else:
        return 0


def tf_title(bug, term):
    qs = FrequencyTitle.objects.filter(bug=bug, term=term)
    if qs.count() > 0:
        return qs.first().freq
    else:
        return 0


def tf_detail(bug, term):
    qs = FrequencyDetail.objects.filter(bug=bug, term=term)
    if qs.count() > 0:
        return qs.first().freq
    else:
        return 0


# The IDFs

def idf(term):
    Da = BugReport.objects.count()
    Dt = Frequency.objects.filter(term=term).count()
    return n.log2(Da / (1 + Dt))


def idf_title(term):
    Da = BugReport.objects.count()
    Dt = FrequencyTitle.objects.filter(term=term).count()
    return n.log2(Da / (1 + Dt))


def idf_detail(term):
    Da = BugReport.objects.count()
    Dt = FrequencyDetail.objects.filter(term=term).count()
    return n.log2(Da / (1 + Dt))


# The similarities

def similarity(text1, text2, idf_func=idf):
    common = set(tokenize(text1)).intersection(set(tokenize(text2)))
    return n.sum([idf_func(w) for w in common])
