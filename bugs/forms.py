from django.forms import ModelForm

from .models import BugReport


class BugReportForm(ModelForm):

    class Meta:
        model = BugReport
        exclude = ['created', 'updated', 'submitter']
