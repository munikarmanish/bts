from bugs.models import BugReport
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class FrequencyTitle(models.Model):
    bug = models.ForeignKey(BugReport, related_name='title_frequencies', on_delete=models.CASCADE)
    term = models.CharField('Term', max_length=100, db_index=True)
    freq = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = (('bug', 'term'),)

    @python_2_unicode_compatible
    def __str__(self):
        s = "FrequencyTitle(#{bug}, '{term}') = {freq}"
        return s.format(
            bug=self.bug.id,
            term=self.term,
            freq=self.freq)


class FrequencyDetail(models.Model):
    bug = models.ForeignKey(BugReport, related_name='detail_frequencies', on_delete=models.CASCADE)
    term = models.CharField('Term', max_length=100, db_index=True)
    freq = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = (('bug', 'term'),)

    @python_2_unicode_compatible
    def __str__(self):
        s = "FrequencyDetail(#{bug}, '{term}') = {freq}"
        return s.format(
            bug=self.bug.id,
            term=self.term,
            freq=self.freq)


class Frequency(models.Model):
    bug = models.ForeignKey(BugReport, related_name='frequencies', on_delete=models.CASCADE)
    term = models.CharField('Term', max_length=100, db_index=True)
    freq = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = (('bug', 'term'),)

    @python_2_unicode_compatible
    def __str__(self):
        s = "Frequency(#{bug}, '{term}') = {freq}"
        return s.format(
            bug=self.bug.id,
            term=self.term,
            freq=self.freq)
