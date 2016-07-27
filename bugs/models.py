from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
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
    SEVERITY_IMMEDIATE = 5

    SEVERITY_CHOICES = (
        (SEVERITY_LOW, 'Low'),
        (SEVERITY_NORMAL, 'Normal'),
        (SEVERITY_HIGH, 'High'),
        (SEVERITY_URGENT, 'Urgent'),
        (SEVERITY_IMMEDIATE, 'Immediate'),
    )

    # Status choices
    STATUS_NEW = 0
    STATUS_MASTER = 1
    STATUS_DUPLICATE = 2

    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_MASTER, 'Master'),
        (STATUS_DUPLICATE, 'Duplicate'),
    )

    # Timestamps
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Core important fields
    title = models.CharField(max_length=255)
    submitter = models.ForeignKey(User)

    # Versions
    os = models.CharField(blank=True, max_length=100, verbose_name='Operating system')
    ram = models.CharField(blank=True, max_length=100, verbose_name='RAM')
    gpu = models.CharField(blank=True, max_length=100, verbose_name='GPU')
    cuda_cores = models.CharField(blank=True, max_length=100, verbose_name='CUDA cores')
    vram = models.CharField(blank=True, max_length=100, verbose_name='Video RAM')

    # Filterable fields
    category = models.ForeignKey(BugCategory)
    severity = models.SmallIntegerField(choices=SEVERITY_CHOICES, default=SEVERITY_NORMAL)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_NEW)
    is_solved = models.BooleanField(default=False)

    # Description fields
    project = models.CharField(blank=True, max_length=100, verbose_name='Project title')
    particle = models.CharField(blank=True, max_length=100, verbose_name='Particle number')
    triangle = models.CharField(blank=True, max_length=100, verbose_name='Triangle number')
    description = models.TextField()
    reproduce = models.TextField(blank=True, verbose_name='Steps to reproduce')
    actual = models.TextField(blank=True, verbose_name='Actual behavior')
    expected = models.TextField(blank=True, verbose_name='Expected behavior')

    # Fields for algorithms
    master = models.ForeignKey('self', null=True, blank=True, limit_choices_to={'master': None})

    class Meta:
        verbose_name = 'Bug report'
        verbose_name_plural = 'Bug reports'

    @python_2_unicode_compatible
    def __str__(self):
        title = "[#{id}] {title}"
        return title.format(id=self.id, title=Truncator(self.title).chars(30))

    def get_absolute_url(self):
        return reverse('bugs_detail', kwargs={'id': self.id})

    def similarity(bug):
        return token_similarity(tokenize(self.title), tokenize(bug.title))

    def get_similar_reports(self, n=10):
        from .utils import bug_similarity

        masters = BugReport.objects.filter(master=None, category=self.category, project=self.project)
        candidates = []
        max_sim = bug_similarity(self, self)
        for bug in masters:
            candidates.append((bug_similarity(self, bug), bug.id))
        id_and_sim = [(two, one * 100 / max_sim)
                      for (one, two) in sorted(candidates, reverse=True)[1:min(n, len(candidates))]]
        bug_and_sim = [(BugReport.objects.get(id=id), sim) for id, sim in id_and_sim]
        return bug_and_sim
