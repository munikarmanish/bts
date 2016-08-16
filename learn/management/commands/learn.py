import itertools
import pickle

import numpy as np
from bugs.models import BugCategory, BugReport
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from info.utils import feature_set, idf, idf_detail, idf_title, similarity
from learn.utils import LearningModel


def get_training_row(bug1, bug2, y):
    row = feature_set(bug1, bug2)
    row.append(y)
    return row


class Command(BaseCommand):
    help = "Learn from the current set of bug reports"

    def handle(self, *args, **options):

        data = []  # This will finally end up as the training sample

        masters = BugReport.objects.filter(master=None)
        print("There are {} masters.".format(masters.count()))

        # Create positive training data
        for master in masters:
            for duplicate in master.duplicates.all():
                data.append(get_training_row(master, duplicate, 1))
        print("Generated {} positive samples.".format(len(data)))

        # Create negative training data
        for bug1, bug2 in itertools.combinations(masters, 2):
            data.append(get_training_row(bug1, bug2, 0))

        data = np.matrix(data)
        print("Total size of training data: {}".format(data.shape))
        np.savetxt('training.csv', data)

        model = LearningModel()
        model.learn(data)
        model.save()

        print("Successfully learned!")
