from django.conf.urls import url

from . import signals
from .views import BugAdd, BugDetail, BugList, BugUpdate

urlpatterns = [
    url(r'^$', BugList.as_view(), name='bugs_list'),
    url(r'^(?P<id>\d+)/$', BugDetail.as_view(), name='bugs_detail'),
    url(r'^(?P<id>\d+)/update/$', BugUpdate.as_view(), name='bugs_update'),
    url(r'^add/$', BugAdd.as_view(), name='bugs_add'),
]
