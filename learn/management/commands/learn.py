from django.conf import settings
from django.core.management.base import BaseCommand

from learn.utils import LearningModel


class Command(BaseCommand):
    help = 'Learn from the current set of bug reports'

    def handle(self, *args, **options):
        model = LearningModel()
        self.stdout.write("Test command")
