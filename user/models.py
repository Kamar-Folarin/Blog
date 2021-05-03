from django.db import models
from django.contrib.auth.signals import user_logged_out
from django.contrib import messages


def logout_message(sender, user, request, **kwargs):
    messages.success(request, "You are logged out ")


user_logged_out.connect(logout_message)
