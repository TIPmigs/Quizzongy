from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.db import IntegrityError

User = get_user_model()

def check_username(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return  # Skip if user already exists (logging in)

    # Extract relevant data
    email = details.get('email')
    username = details.get('username') or details.get('login')
    extra_data = kwargs.get('response', {})
    github_id = str(extra_data.get('id'))

    # Fallback if GitHub username is None
    if not username:
        username = f"github_user_{github_id}"

    # Ensure username is unique
    from core.models import CustomUser
    original_username = username
    counter = 1
    while CustomUser.objects.filter(username=username).exists():
        username = f"{original_username}_{counter}"
        counter += 1

    # Save temporary data for user creation
    strategy.session_set('github_username', username)
    strategy.session_set('github_id', github_id)
    
# Optional: extend user_details to save github_id
def save_github_id(backend, user, response, *args, **kwargs):
    github_id = response.get('id')
    if github_id and not user.github_id:
        user.github_id = github_id
        user.save()



def associate_by_github_id(strategy, details, backend, uid, user=None, *args, **kwargs):
    from core.models import CustomUser

    if backend.name == 'github':
        try:
            existing_user = CustomUser.objects.get(github_id=uid)
            return {'is_new': False, 'user': existing_user}
        except CustomUser.DoesNotExist:
            return None
