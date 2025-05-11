# yourapp/pipeline.py

from django.shortcuts import redirect

def check_username(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and is_new and not user.username:
        # Store partial pipeline state
        return redirect('set_username')
