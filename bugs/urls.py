from django.conf.urls import url

from . import signals
from .views import BugDetail, BugList

urlpatterns = [
    url(r'^$', BugList.as_view(), name='bugs_list'),
    url(r'^(?P<id>\d+)/', BugDetail.as_view(), name='bugs_detail'),
]
