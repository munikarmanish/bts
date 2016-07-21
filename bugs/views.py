from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import BugCategory, BugReport


class BugList(ListView):
    context_object_name = 'bugs'
    model = BugReport
    page_kwarg = 'page'
    paginate_by = 30
    template_name = 'bugs/list.html'


class BugDetail(DetailView):
    model = BugReport
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'bugs/detail.html'
    context_object_name = 'bug'
