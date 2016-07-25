from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def user_logged_in_receiver(sender, request, user, **kwargs):
    messages.success(request, "Successfully logged in!")


@receiver(user_logged_out)
def user_logged_out_receiver(sender, request, user, **kwargs):
    messages.success(request, "Successfully logged out!")
