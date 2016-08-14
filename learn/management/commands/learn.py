from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Test command'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Successfully learned!'))
