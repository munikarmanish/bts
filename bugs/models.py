import os

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import Truncator


class BugCategory(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Bug category'
        verbose_name_plural = 'Bug categories'
        ordering = ['name', ]

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class BugReport(models.Model):

    # Severity choices
    SEVERITY_LOW = 1
    SEVERITY_NORMAL = 2
    SEVERITY_HIGH = 3
    SEVERITY_URGENT = 4
    SEVERITY_FEATURE = 0

    SEVERITY_CHOICES = (
        (SEVERITY_LOW, 'Low'),
        (SEVERITY_NORMAL, 'Normal'),
        (SEVERITY_HIGH, 'High'),
        (SEVERITY_URGENT, 'Urgent'),
        (SEVERITY_FEATURE, 'Feature'),
    )

    # Status choices
    STATUS_NEW = 0
    STATUS_REJECTED = 1
    STATUS_ASSIGNED = 2
    STATUS_FIXED = 3

    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_ASSIGNED, 'Assigned'),
        (STATUS_FIXED, 'Fixed'),
    )

    # Timestamps
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Core important fields
    title = models.CharField(max_length=255)
    submitter = models.ForeignKey(User, related_name='submitted_reports')

    # Versions
    os = models.CharField(blank=True, max_length=100, verbose_name='Operating system')
    ram = models.CharField(blank=True, max_length=100, verbose_name='RAM')
    vram = models.CharField(blank=True, max_length=100, verbose_name='Video RAM')

    # Filterable fields
    category = models.ForeignKey(BugCategory)
    severity = models.SmallIntegerField(choices=SEVERITY_CHOICES, default=SEVERITY_NORMAL)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_NEW)

    # Description fields
    expected = models.TextField(blank=True, verbose_name='Expected behavior')
    actual = models.TextField(blank=True, verbose_name='Actual behavior')
    reproduce = models.TextField(blank=True, verbose_name='Steps to reproduce')

    # Fields for algorithms
    master = models.ForeignKey(
        'self', related_name='duplicates', null=True, blank=True, limit_choices_to={'master': None})

    # Solution
    assignee = models.ForeignKey(
        User, related_name='assigned_reports', null=True, blank=True,
        limit_choices_to={'is_staff': True})
    solution = models.TextField(blank=True, null=True, verbose_name='Solution')

    class Meta:
        verbose_name = 'Bug report'
        verbose_name_plural = 'Bug reports'
        ordering = ['-created', ]

    @python_2_unicode_compatible
    def __str__(self):
        title = "[#{id}] {title}"
        return title.format(id=self.id, title=Truncator(self.title).chars(100))

    def get_absolute_url(self):
        return reverse('bugs_detail', kwargs={'id': self.id})

    def is_fixed(self):
        return self.status == STATUS_FIXED

    def detail_text(self):
        return " ".join([self.os, self.ram, self.vram, self.expected, self.actual, self.reproduce])

    def all_text(self):
        return " ".join([self.title, self.detail_text()])

    def get_similar_reports(self, n=10):
        from info.utils import similarity, idf, idf_detail, idf_title

        candidates = []
        max_sim = similarity(self.all_text(), self.all_text())
        for bug in BugReport.objects.filter(category=self.category):
            candidates.append((similarity(self.all_text(), bug.all_text()), bug.id))
        id_and_sim = [(two, one * 100 / max_sim)
                      for (one, two) in sorted(candidates, reverse=True)[1:min(n, len(candidates))]]
        bug_and_sim = [(BugReport.objects.get(id=id), sim) for id, sim in id_and_sim]
        return bug_and_sim

    def get_possible_duplicates(self, n=10):
        from info.utils import feature_set
        from learn.utils import LearningModel

        model = LearningModel()

        candidates_sim = []
        for b in BugReport.objects.filter(Q(category=self.category), ~Q(id=self.id)):
            candidates_sim.append((model.predict(feature_set(self, b)), b.id))
        bug_sim = [(BugReport.objects.get(id=id), sim * 100)
                   for sim, id in sorted(candidates_sim, reverse=True)[:min(n, len(candidates_sim))]]
        return bug_sim


class Attachment(models.Model):
    bug = models.ForeignKey(BugReport, related_name='attachments')
    attachment = models.ImageField(height_field='height', width_field='width')
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'

    def filename(self):
        return os.path.basename(self.attachment.name)

    def fullpath(self):
        return self.attachment.name

    @python_2_unicode_compatible
    def __str__(self):
        return self.filename()
