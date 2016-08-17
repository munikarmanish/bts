from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import DetailView, FormView

from .forms import RegistrationForm


class Register(FormView):
    """Registration (Signup) view."""

    form_class = RegistrationForm
    success_url = '/'
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully registered!')
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(Register, self).form_valid(form)


class ProfileView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'accounts/profile.html'
    context_object_name = 'user'
