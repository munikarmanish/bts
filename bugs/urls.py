from django.conf.urls import url

from . import signals
from .views import BugAdd, BugDetail, BugList

urlpatterns = [
    url(r'^$', BugList.as_view(), name='bugs_list'),
    url(r'^(?P<id>\d+)/', BugDetail.as_view(), name='bugs_detail'),
    url(r'^add/$', BugAdd.as_view(), name='bugs_add'),
]
