from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from social_django.models import UserSocialAuth
import requests 
from django.conf import settings
from .forms import CustomUserRegisterForm, CustomLoginForm
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from core.models import CustomUser 
from django.contrib.auth.decorators import login_required

#LANDING VIEW
def landing(request):
    return render(request, 'authentication/landing.html')

def register(request):
    return render(request, 'authentication/register.html')

#LOGOUT VIEW
def logout_view(request):
    if request.user.is_authenticated:
        revoke_github_token(request.user)
        request.user.social_auth.filter(provider='github').delete()
        logout(request)
    return redirect('/')

#REVOKE GITHUB TOKEN FOR REAUTHENTICATION
def revoke_github_token(user):
    try:
        social = user.social_auth.get(provider='github')
        access_token = social.extra_data.get('access_token')

        if access_token:
            requests.delete(
                f'https://api.github.com/applications/{settings.SOCIAL_AUTH_GITHUB_KEY}/grant',
                auth=(settings.SOCIAL_AUTH_GITHUB_KEY, settings.SOCIAL_AUTH_GITHUB_SECRET),
                json={'access_token': access_token}
            )
    except Exception as e:
        print("Error revoking GitHub token:", e)

#DASHBOARD VIEW
@login_required
def dashboard(request):
    return render(request, 'student/Dashboard.html')
 
#REGISTER VIEW
def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(f"""
                <script>
                    alert('Account created successfully!');
                    window.location.href = '{reverse('login')}';
                </script>
            """)
    else:
        form = CustomUserRegisterForm()
    return render(request, 'authentication/register.html', {'form': form})

#LOGIN VIEW
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Assuming this is your landing page after login
        else:
            return render(request, 'authentication/login.html', {
                'form': {'username': username},
                'error': 'Invalid username or password'
            })

    return render(request, 'authentication/login.html', {'form': {}})