from django import forms
from multiupload.fields import MultiImageField

from .models import BugCategory, BugReport


class BugReportForm(forms.ModelForm):
    images = MultiImageField(
        label='Images',
        max_num=3,
        max_file_size=1024 * 1024 * 10,
        required=False,
    )

    class Meta:
        model = BugReport
        exclude = ['created', 'status', 'updated', 'submitter', 'solution', 'is_solved', 'master']


class FilterForm(forms.Form):

    SEVERITY_CHOICES = [('', '---------'), ]
    SEVERITY_CHOICES.extend(BugReport.SEVERITY_CHOICES)
    STATUS_CHOICES = [('', '---------'), ]
    STATUS_CHOICES.extend(BugReport.STATUS_CHOICES)

    category = forms.ModelChoiceField(
        queryset=BugCategory.objects.all().order_by('name'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    severity = forms.ChoiceField(
        choices=SEVERITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
