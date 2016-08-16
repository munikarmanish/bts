from bugs.models import BugCategory, BugReport
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from info.utils import idf, idf_detail, idf_title, similarity
from learn.utils import LearningModel


class Command(BaseCommand):
    help = 'Learn from the current set of bug reports'

    def handle(self, *args, **options):
        model = LearningModel()

        non_duplicates = BugReport.objects.filter(master=None)
        duplicates = BugReport.objects.filter(~Q(master=None))

        print("DUPLICATES::")
        for bug in duplicates:
            print(bug)

        print("NON_DUPLICATES::")
        for bug in non_duplicates:
            print(bug)
