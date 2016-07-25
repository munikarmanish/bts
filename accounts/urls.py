from django.conf.urls import include, url
from django.contrib.auth.views import login, logout

from . import signals
from .views import Register

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
]
