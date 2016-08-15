import string

import numpy as n
from django.db.models import Count
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from info.models import Frequency, FrequencyDetail, FrequencyTitle

from .models import BugCategory, BugReport


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


def token_similarity(tokens1, tokens2):
    common = set(tokens1).intersection(set(tokens2))
    return n.sum([idf(w) for w in common])


def bug_similarity(bug1, bug2):
    return token_similarity(tokenize(bug1.title), tokenize(bug2.title))
