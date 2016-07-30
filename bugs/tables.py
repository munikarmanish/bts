import django_tables2 as tables

from .models import BugReport


class BugReportTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    title = tables.RelatedLinkColumn(verbose_name='Title')
    project = tables.Column(verbose_name='Project')
    category = tables.Column(verbose_name='Category')
    severity = tables.Column(verbose_name='Severity')
    created = tables.DateColumn(verbose_name='Created')
    status = tables.Column(verbose_name='Status')

    class Meta:
        model = BugReport
        attrs = {'class': 'table table-condensed'}
        fields = ['id', 'title', 'project', 'category', 'severity', 'created', 'status']
        pagination = False
