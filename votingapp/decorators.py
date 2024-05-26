# decorators.py
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

def authorized_user_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.username not in settings.AUTHORIZED_USERS:
            messages.error(request, 'You are not authorized to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
