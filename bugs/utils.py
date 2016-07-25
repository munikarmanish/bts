import string

import numpy as n
from django.db.models import Count
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from info.models import Frequency

from .models import BugCategory, BugReport


def tokenize(text):
    lowers = text.lower()
    punct_free = lowers.translate(str.maketrans({key: None for key in string.punctuation}))
    tokens = word_tokenize(punct_free)
    porter = PorterStemmer()
    stemmed = [porter.stem(w) for w in tokens]
    tokens = [w for w in stemmed if w not in stopwords.words('english')]
    return tokens


def idf(term):
    Da = BugReport.objects.count()
    Dt = Frequency.objects.filter(term=term).count()
    return n.log2(Da / (1 + Dt))


def token_similarity(tokens1, tokens2):
    common = set(tokens1).intersection(set(tokens2))
    return n.sum([idf(w) for w in common])


def bug_similarity(bug1, bug2):
    return token_similarity(tokenize(bug1.title), tokenize(bug2.title))
