from bugs.models import BugReport
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
class Frequency(models.Model):
    bug = models.ForeignKey(BugReport)
    term = models.CharField('Term', max_length=100, db_index=True)
    freq = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = (('bug', 'term'),)

    @python_2_unicode_compatible
    def __str__(self):
        s = "(#{bug}, '{term}' = {freq})"
        return s.format(
            bug=self.bug.id,
            term=self.term,
            freq=self.freq)
