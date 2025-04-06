from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            default_group = Group.objects.filter(name="User").first()
            if default_group:
                user.groups.add(default_group)

            return render(request, 'accounts/activation_sent.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def activate_account(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse('Invalid user_id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found or activation period expired')



def login_redirect(request):
    """Redirect users to their respective dashboards after login."""
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    elif user.groups.filter(name="Organizer").exists():
        return redirect('organizer_dashboard')
    else:
        return redirect('user_dashboard')

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return login_redirect(request)
            else:
                messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")