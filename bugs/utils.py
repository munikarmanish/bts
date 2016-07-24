import string

import numpy as n
import sklearn as sk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from .models import BugCategory, BugReport


def tokenize(text):
    lowers = text.lower()
    punct_free = lowers.translate(str.maketrans({key: None for key in string.punctuation}))
    tokens = word_tokenize(lowers)
    porter = PorterStemmer()
    stemmed = [porter.stem(w) for w in tokens]
    tokens = [w for w in tokens if w not in stopwords.words('english')]
    return stemmed


def dterm(term):
    bugs = BugReport.objects.filter(title__icontains=term)
    n = 0
    for bug in bugs:
        if term in tokenize(bug.title):
            n += 1
    return n


def idf(term):
    Da = len(BugReport.objects.all())
    Dt = dterm(term)
    return n.log2(Da / (1 + Dt))


def token_similarity(tokens1, tokens2):
    common = set(tokens1).intersection(set(tokens2))
    return n.sum([idf(w) for w in common])


def bug_similarity(bug1, bug2):
    return token_similarity(tokenize(bug1.title), tokenize(bug2.title))
