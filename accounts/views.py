from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import FormView

from .forms import RegistrationForm


class Register(FormView):
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
