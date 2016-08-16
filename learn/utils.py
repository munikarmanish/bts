import pickle

import numpy as n
import scipy.optimize as o
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from numpy import array, exp, log, matrix, multiply


def h(theta, x):  # `theta` and `x` are assumed to be matrix
    return 1 / (1 + n.exp(-(x.T * theta)))


def cost(hx, y):  # All arguments are assumed to be matrix
    return -(multiply(y, log(hx)) + multiply((1 - y), log(1 - hx)))


def cost_function(theta, X, y):  # All arguments are assumed to be matrix
    return (1.0 / y.size) * n.sum(cost(h(theta, X.T), y))


class LearningModel(object):

    theta = None  # This will be in matrix form
    filename = settings.BASE_DIR + "/model.pickle"

    def __init__(self):
        super(LearningModel, self).__init__()
        self.read()

    @python_2_unicode_compatible
    def __str__(self):
        return str(self.theta)

    def read(self):
        try:
            with open(self.filename, 'rb') as f:
                model = pickle.load(f)
                self.theta = model.theta
                return self
        except FileNotFoundError:
            self.save()

    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self, f)
            return self

    def predict(self, input_set):
        # Add x0 = 1
        x = n.insert(n.array(input_set), 0, 1)
        # Convert to column matrix
        x = n.matrix(x).T
        # Calculate the probability
        return h(self.theta, x).item(0)

    def h(self, x):
        return self.predict(x)

    def learn(self, training_set):
        data = n.matrix(training_set)
        m = data.shape[0]
        X = n.concatenate((n.ones((m, 1)), data[:, 0:-1]), axis=1)
        y = data[:, -1]

        def J(theta):  # Decorator to use for o.minimize()
            return cost_function(n.matrix(theta).T, X, y)

        # This is the meat of the learning algorithm
        result = o.minimize(J, self.theta.A1)
        self.theta = n.matrix(result.x).T
        self.save()
