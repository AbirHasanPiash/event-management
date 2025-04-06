from django.urls import path
from .views import signup_view, login_view, logout_view, login_redirect, activate_account

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('activate/<int:user_id>/<str:token>/', activate_account, name='activate'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path('dashboard/', login_redirect, name='dashboard_redirect'),
]
