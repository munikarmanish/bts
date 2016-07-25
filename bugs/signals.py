from django.db.models.signals import post_save
from django.dispatch import receiver

from info.models import Frequency

from .models import BugReport
from .utils import tokenize


@receiver(post_save, sender=BugReport)
def bug_report_post_save(sender, instance, created, **kwargs):
    terms = tokenize(instance.title)
    for t in set(terms):
        values = {'freq': terms.count(t)}
        Frequency.objects.update_or_create(bug=instance, term=t, defaults=values)
