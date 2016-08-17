import pickle

import numpy as n
import scipy.optimize as o
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from numpy import array, exp, log, matrix, multiply


def h(theta, x):
    """Returns the result of prediction function of logistic regression.

    Parameters
    ----------
    theta : matrix of shape (n, 1)
        The weight paramters
    x : matrix (n, *)
        The input matrix

    Returns
    -------
    h = sigmoid(x.T * theta)
    """
    hx = 1 / (1 + n.exp(-(x.T * theta)))
    if hx.max() == 1:
        print(hx)
        raise Exception("GOT ONE!")
    return hx


def cost(hx, y):
    """Returns the cost of logistic regression using the formula:

        cost = -y.log(hx) - (1-y).log(1-hx)

    Parameters
    ----------
    hx : float
        Predicted value
    y : int
        Real value
    """
    return -n.multiply(n.round(y), n.log(hx)) - n.multiply((1 - n.round(y)), n.log(1 - hx))


def cost_function(theta, X, y, l=0.5):
    """Returns the regularized cost of current learned weight parameters.

    Parameters
    ----------
    theta : matrix (n, 1)
        Weight parameters
    X : matrix (m, n)
        Training input set
    y : matrix (m, 1)
        Training output set
    l : float
        Regularization parameter
    """
    return (1.0 / y.size) * n.sum(cost(h(theta, X.T), y)) + (l / y.size) * n.sum(theta.A**2)


# def cost_gradient(theta, X, y, l=0.5):
#     """Returns an array of first partial derivatives of cost functions
#     w.r.t theta.
#
#     Parameters
#     ----------
#     theta : matrix (n, 1)
#         Weight parameters
#     X : matrix (m, n)
#         Training input set
#     y : matrix (m, 1)
#         Training output set
#     l : float
#         Regularization parameter
#     """
#     result = [(1.0 / y.size) * n.sum(n.multiply(h(theta, X.T) - y, X[:, 0]))]
#     for j in range(1, len(theta)):
#         dj = (1.0 / y.size) * (n.sum(n.multiply(h(theta, X.T) - y, X[:, j])) + (2 * l * theta.item(j)))
#         result.append(dj)
#     return n.array(result)


class LearningModel(object):
    """Linear, regularized, binary logistic regression learning model.
    """
    theta = None  # Column matrix
    maxs = None  # Column matrix
    filename = settings.BASE_DIR + "/model.pickle"

    def __init__(self):
        super(LearningModel, self).__init__()
        self.read()

    @python_2_unicode_compatible
    def __str__(self):
        return str(self.theta)

    def read(self):
        """Read the model file and update self.
        """
        try:
            with open(self.filename, 'rb') as f:
                model = pickle.load(f)
                self.theta = model.theta
                self.maxs = model.maxs
                return self
        except FileNotFoundError:
            self.save()

    def save(self):
        """Save self to the model file for future reference.
        """
        with open(self.filename, 'wb') as f:
            pickle.dump(self, f)
            return self

    def predict(self, input_set):
        """Predicts the output for given input set using learned model.

        Parameters
        ----------
        input_set : list | array
            List of (n-1) features. The first feature is always 1.
        """
        # Add x0 = 1
        x = n.insert(n.array(input_set), 0, 1)
        # Convert to column matrix
        x = n.matrix(x).T
        # Calculate the probability
        return h(self.theta, x / self.maxs).item()

    # def h(self, x):
    #     return self.predict(x)

    def learn(self, training_set):
        """Learn from the given training data.

        Parameters
        ----------
        training_set : matrix (m, n)
            The total training matrix (including the output, excluding bias column)
        """
        # n.seterr(all='raise') # Uncomment this to raise exceptions for floating point errors

        data = n.matrix(training_set)
        m = data.shape[0]
        X = n.concatenate((n.ones((m, 1)), data[:, 0:-1]), axis=1)
        self.maxs = X.max(axis=0).T
        Xn = X / X.max(0)
        y = data[:, -1]

        def J(theta):  # Decorator to use for o.minimize()
            """Decorator of cost_function() to use for minimize().

            Parameters
            ----------
            theta : list | array (n)
                Weight parameters
            """
            return cost_function(n.matrix(theta).T, Xn, y)

        # def DJ(theta):
        #     """Decorator of cost_gradient() to use for minimize().
        #
        #     Parameters
        #     ----------
        #     theta : list | array (n)
        #         Weight parameters
        #     """
        #     return cost_gradient(n.matrix(theta).T, Xn, y)

        # This is the meat of the learning algorithm
        initial_theta = n.zeros(X.shape[1])
        result = o.minimize(J, initial_theta)
        print(result)
        self.theta = n.matrix(result.x).T
        self.save()

        return result
