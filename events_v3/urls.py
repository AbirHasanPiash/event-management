from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='user_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('organizer-dashboard/', views.OrganizerDashboardView.as_view(), name='organizer_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-groups/', views.manage_groups, name='manage_groups'),
    path('groups/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('groups/add/', views.add_group, name='add_group'),
    path('groups/<int:group_id>/assign-permissions/', views.assign_permissions, name='assign_permissions'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:user_id>/assign-role/', views.assign_role, name='assign_role'),
    path('no-permission/', views.no_permission_view, name='no-permission'),

    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/update/', views.event_update, name='event_update'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    path('events/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('events/<int:event_id>/cancel-rsvp/', views.cancel_rsvp, name='cancel_rsvp'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
