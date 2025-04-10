from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignupView, LoginView, logout_view, login_redirect, ActivateAccountView, CustomPasswordChangeView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('activate/<int:user_id>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),

    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('dashboard/', login_redirect, name='dashboard_redirect'),
]
