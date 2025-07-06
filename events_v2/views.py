from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Category
from .forms import EventForm, CategoryForm
from django.contrib import messages
<<<<<<<< HEAD:events_v2/views.py
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Count, Q, Prefetch
========
from django.contrib.auth.models import Group, Permission
from django.db.models import Count, Q
>>>>>>>> mid-term-exam:events_v3/views.py
from django.utils.dateparse import parse_date
from django.utils.timezone import now, localtime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserChangeForm
from django.views import View


User = get_user_model()


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()

def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()

def is_admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)

def is_user(user):
    return user.groups.filter(name="User").exists()


def home(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
<<<<<<<< HEAD:events_v2/views.py
========

>>>>>>>> mid-term-exam:events_v3/views.py
    events = Event.objects.select_related('category')

    if query:
        events = events.filter(name__icontains=query)
    
    if category_filter:
        events = events.filter(category_id=category_filter)
    
    if start_date and end_date:
        events = events.filter(date__range=[parse_date(start_date), parse_date(end_date)])

    events = events.annotate(participant_count=Count('participants')).prefetch_related('participants')

    categories = Category.objects.only('id', 'name')

    return render(request, 'events/home.html', {
        'events': events,
        'categories': categories,
        'query': query,
        'category_filter': category_filter,
        'start_date': start_date,
        'end_date': end_date
    })

<<<<<<<< HEAD:events_v2/views.py
# @login_required
# @user_passes_test(is_organizer, login_url='no-permission')
# def organizer_dashboard(request):
#     today = now().date()

#     events = Event.objects.prefetch_related('participants') \
#                           .annotate(participant_count=Count('participants', distinct=True))

#     total_participants = Event.objects.aggregate(total_sum=Count('participants'))['total_sum']

#     event_counts = Event.objects.aggregate(
#         total=Count('id'),
#         upcoming=Count('id', filter=Q(date__gte=today)),
#         past=Count('id', filter=Q(date__lt=today))
#     )

#     todays_events = events.filter(date=today)

#     filter_type = request.GET.get('filter', 'all')
#     if filter_type == "upcoming":
#         filtered_events = events.filter(date__gte=today)
#     elif filter_type == "past":
#         filtered_events = events.filter(date__lt=today)
#     else:
#         filtered_events = events

#     return render(request, 'accounts/organizer_dashboard.html', {
#         'total_participants': total_participants,
#         'total_events': event_counts['total'],
#         'upcoming_events': event_counts['upcoming'],
#         'past_events': event_counts['past'],
#         'todays_events': todays_events,
#         'events': filtered_events,
#         'filter_type': filter_type
#     })
========

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        user_groups = user.groups.all().only('name')

        context['user_info'] = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'date_joined': localtime(user.date_joined).strftime("%B %d, %Y, %I:%M %p"),
            'last_login': localtime(user.last_login).strftime("%B %d, %Y, %I:%M %p") if user.last_login else "Never",
            'groups': [group.name for group in user_groups],
        }
        return context


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


class OrganizerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not is_organizer(request.user):
            return redirect('no-permission')
        return super().dispatch(request, *args, **kwargs)


class OrganizerDashboardView(LoginRequiredMixin, OrganizerRequiredMixin, View):
    def get(self, request):
        today = now().date()

        base_events_qs = Event.objects.select_related('category') \
                                      .prefetch_related('participants') \
                                      .annotate(participant_count=Count('participants', distinct=True))

        filter_type = request.GET.get('filter', 'all')
        if filter_type == "upcoming":
            filtered_events = base_events_qs.filter(date__gte=today)
        elif filter_type == "past":
            filtered_events = base_events_qs.filter(date__lt=today)
        else:
            filtered_events = base_events_qs

        todays_events = base_events_qs.filter(date=today)

        total_participants = Event.objects.aggregate(total_sum=Count('participants'))['total_sum']

        event_counts = base_events_qs.aggregate(
            total=Count('id'),
            upcoming=Count('id', filter=Q(date__gte=today)),
            past=Count('id', filter=Q(date__lt=today))
        )

        context = {
            'total_participants': total_participants,
            'total_events': event_counts['total'],
            'upcoming_events': event_counts['upcoming'],
            'past_events': event_counts['past'],
            'todays_events': todays_events,
            'events': filtered_events,
            'filter_type': filter_type
        }

        return render(request, 'accounts/organizer_dashboard.html', context)

>>>>>>>> mid-term-exam:events_v3/views.py

@login_required
@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):
    today = now().date()

<<<<<<<< HEAD:events_v2/views.py
    # Base queryset optimized
========
>>>>>>>> mid-term-exam:events_v3/views.py
    base_events_qs = Event.objects.select_related('category') \
                                   .prefetch_related('participants') \
                                   .annotate(participant_count=Count('participants', distinct=True))

<<<<<<<< HEAD:events_v2/views.py
    # Use base queryset for all filtered versions
========
>>>>>>>> mid-term-exam:events_v3/views.py
    filter_type = request.GET.get('filter', 'all')
    if filter_type == "upcoming":
        filtered_events = base_events_qs.filter(date__gte=today)
    elif filter_type == "past":
        filtered_events = base_events_qs.filter(date__lt=today)
    else:
        filtered_events = base_events_qs

<<<<<<<< HEAD:events_v2/views.py
    # Today's events (reuse base queryset to preserve annotations)
    todays_events = base_events_qs.filter(date=today)

    # Total participants (use distinct count on base queryset)
    total_participants = total_participants = Event.objects.aggregate(total_sum=Count('participants'))['total_sum']


    # Event counts
========
    todays_events = base_events_qs.filter(date=today)

    total_participants = total_participants = Event.objects.aggregate(total_sum=Count('participants'))['total_sum']

>>>>>>>> mid-term-exam:events_v3/views.py
    event_counts = base_events_qs.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gte=today)),
        past=Count('id', filter=Q(date__lt=today))
    )

    return render(request, 'accounts/organizer_dashboard.html', {
        'total_participants': total_participants,
        'total_events': event_counts['total'],
        'upcoming_events': event_counts['upcoming'],
        'past_events': event_counts['past'],
        'todays_events': todays_events,
        'events': filtered_events,
        'filter_type': filter_type
    })

def no_permission_view(request):
    return render(request, 'accounts/no_permission.html')

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not is_admin(request.user):
            return redirect('no-permission')
        return super().dispatch(request, *args, **kwargs)


class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        users_count = User.objects.count()
        groups_count = Group.objects.count()

        total_users = users_count
        total_events = Event.objects.count()
        total_categories = Category.objects.count()

        context = {
            'users_count': users_count,
            'groups_count': groups_count,
            'total_users': total_users,
            'total_events': total_events,
            'total_categories': total_categories,
        }

        return render(request, 'accounts/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def manage_users(request):
    users = User.objects.prefetch_related('groups').all()
    return render(request, 'accounts/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, 'User updated successfully.')
            return redirect('manage_users')

    return render(request, 'accounts/edit_user.html', {
        'user_obj': user,
    })

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('manage_users')

    return render(request, 'accounts/delete_user.html', {
        'user_obj': user,
    })

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def manage_groups(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'accounts/manage_groups.html', {'groups': groups})


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def assign_permissions(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    all_permissions = Permission.objects.all()

    group_permission_ids = set(group.permissions.values_list('id', flat=True))

    if request.method == 'POST':
        selected_permissions = set(map(int, request.POST.getlist('permissions')))
        if selected_permissions != group_permission_ids:
            group.permissions.set(selected_permissions)
            messages.success(request, f'Permissions updated for group: {group.name}')
        else:
            messages.info(request, 'No changes made.')
        return redirect('manage_groups')

    return render(request, 'accounts/assign_permissions.html', {
        'group': group,
        'all_permissions': all_permissions,
        'group_permission_ids': group_permission_ids,
    })


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def add_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            if not Group.objects.filter(name=name).exists():
                Group.objects.create(name=name)
                messages.success(request, f'Group "{name}" has been created successfully.')
                return redirect('manage_groups')  # Replace with your actual URL name
            else:
                messages.error(request, 'A group with this name already exists.')
        else:
            messages.error(request, 'Group name cannot be empty.')
    return render(request, 'accounts/add_group.html')


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.name = request.POST.get('name')
        group.save()
        messages.success(request, 'Group updated successfully!')
        return redirect('manage_groups')
    return render(request, 'accounts/edit_group.html', {'group': group})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted successfully!')
        return redirect('manage_groups')

    return render(request, 'accounts/delete_group.html', {
        'group_obj': group
    })

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = get_object_or_404(User.objects.prefetch_related('groups'), id=user_id)
    all_groups = Group.objects.all()

    if request.method == 'POST':
        selected_group_ids = request.POST.getlist('groups')
        selected_groups = Group.objects.filter(id__in=selected_group_ids)
<<<<<<<< HEAD:events_v2/views.py
        user.groups.clear()
        user.groups.add(*selected_groups)
        user.save()
        messages.success(request, f'Role(s) assigned to {user.username}.')
========
        current_group_ids = set(user.groups.values_list('id', flat=True))
        new_group_ids = set(map(int, selected_group_ids))

        if current_group_ids != new_group_ids:
            user.groups.set(selected_groups)
            messages.success(request, f'Role(s) assigned to {user.username}.')
        else:
            messages.info(request, f'No changes made to {user.username} roles.')

>>>>>>>> mid-term-exam:events_v3/views.py
        return redirect('manage_users')

    return render(request, 'accounts/assign_role.html', {
        'user_obj': user,
        'groups': all_groups,
    })


@login_required
@user_passes_test(is_user, login_url='no-permission')
def user_dashboard(request):
    user = request.user
    events = request.user.rsvp_events.all()
    return render(request, 'accounts/user_dashboard.html', {'events': events, 'user': user})


@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user not in event.participants.all():
        event.participants.add(request.user)
        messages.success(request, 'RSVP successful!')
    return redirect('home')

@login_required
def cancel_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user in event.participants.all():
        event.participants.remove(request.user)
        messages.success(request, 'Your RSVP has been canceled.')
    else:
        messages.info(request, 'You were not RSVPed.')
    return redirect('home')

# Event Views
def event_list(request):
    events = Event.objects.select_related('category') \
                          .prefetch_related('participants') \
                          .only('id', 'name', 'date', 'category', 'image') \
                          .annotate(participant_count=Count('participants', distinct=True))

    return render(request, 'events/event_list.html', {'events': events})

@login_required
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect('event_list')
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form})

def event_detail(request, pk):
    event = get_object_or_404(Event.objects.prefetch_related('participants'), pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            event.delete()
            messages.success(request, "Event deleted successfully.")
            return redirect('event_list')
        else:
            messages.info(request, "Event deletion was canceled.")
            return redirect('event_list')

    return render(request, 'events/event_confirm_delete.html', {'event': event})


@login_required
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def category_list(request):
    categories = Category.objects.only('id', 'name', 'description')
    return render(request, 'categories/category_list.html', {'categories': categories})


@login_required
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.") 
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'categories/category_form.html', {'form': form})


@login_required
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")  # ✅ User feedback
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'categories/category_form.html', {'form': form})


@login_required
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            category.delete()
            messages.success(request, "Category deleted successfully.")
            return redirect('category_list')
        else:
            messages.info(request, "Category deletion was canceled.")
            return redirect('category_list')

    return render(request, 'categories/category_confirm_delete.html', {'category': category})



@login_required
@user_passes_test(is_admin, login_url='no-permission')
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        username = request.POST.get('username', user.username).strip()
        email = request.POST.get('email', user.email).strip()

        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "User updated successfully.")
            return redirect('user_list')
        else:
            messages.error(request, "Username and email cannot be empty.")

    return render(request, 'users/user_form.html', {'user': user})


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            user.delete()
            messages.success(request, "User deleted successfully.")
            return redirect('user_list')
        else:
            messages.info(request, "User deletion was canceled.")
            return redirect('user_list')

    return render(request, 'users/user_confirm_delete.html', {'user': user})

