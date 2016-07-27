from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from .forms import BugReportForm
from .models import BugCategory, BugReport


class BugList(ListView):
    context_object_name = 'bugs'
    model = BugReport
    page_kwarg = 'page'
    # paginate_by = 30
    ordering = '-id'
    template_name = 'bugs/list.html'


class BugDetail(DetailView):
    model = BugReport
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'bugs/detail.html'
    context_object_name = 'bug'


class BugAdd(LoginRequiredMixin, CreateView):
    model = BugReport
    form_class = BugReportForm
    template_name = 'bugs/form.html'

    def get_success_url(self):
        return reverse('bugs_detail', args=(self.object.id,))

    def get_context_data(self, *args, **kwargs):
        context = super(BugAdd, self).get_context_data(*args, **kwargs)
        context['page_title'] = 'Submit New Bug Report'
        return context

    def form_valid(self, form):
        bug = form.save(commit=False)
        bug.submitter = self.request.user
        return super(BugAdd, self).form_valid(form)
