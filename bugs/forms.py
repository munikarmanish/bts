from django import forms

from .models import BugCategory, BugReport


class BugReportForm(forms.ModelForm):

    class Meta:
        model = BugReport
        exclude = ['created', 'updated', 'submitter']


class FilterForm(forms.Form):

    SEVERITY_CHOICES = [('', '---------'), ]
    SEVERITY_CHOICES.extend(BugReport.SEVERITY_CHOICES)
    STATUS_CHOICES = [('', '---------'), ]
    STATUS_CHOICES.extend(BugReport.STATUS_CHOICES)

    category = forms.ModelChoiceField(queryset=BugCategory.objects.all().order_by('name'), required=False)
    severity = forms.ChoiceField(choices=SEVERITY_CHOICES, required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
