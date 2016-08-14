from django import forms
from django.contrib.auth.models import User
from multiupload.fields import MultiImageField

from .fields import UserChoiceField
from .models import BugCategory, BugReport


class BugReportForm(forms.ModelForm):
    images = MultiImageField(
        label='Images',
        max_num=3,
        max_file_size=1024 * 1024 * 10,
        required=False,
    )

    assignee = UserChoiceField(queryset=User.objects.filter(is_staff=True))

    class Meta:
        model = BugReport
        exclude = ['created', 'status', 'updated', 'submitter', 'solution',  'master']


class BugReportUpdateForm(forms.ModelForm):

    assignee = UserChoiceField(queryset=User.objects.filter(is_staff=True))

    class Meta:
        model = BugReport
        fields = ['assignee', 'category', 'severity', 'status', 'master', 'solution']


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
