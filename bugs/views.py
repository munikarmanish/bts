from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django_tables2.config import RequestConfig
from django_tables2.views import SingleTableMixin
from pure_pagination import EmptyPage, PageNotAnInteger, Paginator

from .forms import BugReportForm, FilterForm
from .models import BugCategory, BugReport
from .tables import BugReportTable


class BugList(SingleTableMixin, ListView):
    context_object_name = 'bugs'
    model = BugReport
    page_kwarg = 'page'
    paginator_class = Paginator
    paginate_by = 30
    ordering = '-id'
    template_name = 'bugs/list.html'
    table_class = BugReportTable

    def get_queryset(self):
        q = super(BugList, self).get_queryset()
        # Apply category filter
        category_id = self.request.GET.get('category')
        if category_id:
            q = q.filter(category__id=category_id)
        # Apply project filter
        project = self.request.GET.get('project')
        if project:
            q = q.filter(project=project)
        # Apply severity filter
        severity = self.request.GET.get('severity')
        if severity:
            q = q.filter(severity=severity)
        # Apply status filter
        status = self.request.GET.get('severity')
        if status:
            q = q.filter(status=status)
        # Apply sort
        sort = self.request.GET.get('sort')
        if sort:
            q = q.order_by(sort)
        return q

    def get_context_data(self, **kwargs):
        c = super(BugList, self).get_context_data(**kwargs)
        c['filter_form'] = FilterForm(data=self.request.GET.dict())
        return c


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
