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
