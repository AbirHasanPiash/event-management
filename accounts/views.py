from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class SignupView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('activation_sent')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()

        default_group = Group.objects.filter(name="User").first()
        if default_group:
            user.groups.add(default_group)

        return render(self.request, 'accounts/activation_sent.html')


class ActivateAccountView(View):
    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        return HttpResponse('Invalid user_id or token')



def login_redirect(request):
    """Redirect users to their respective dashboards after login."""
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    elif user.groups.filter(name="Organizer").exists():
        return redirect('organizer_dashboard')
    else:
        return redirect('user_dashboard')

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
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


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('password_change_done')