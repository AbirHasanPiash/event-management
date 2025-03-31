from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from django.contrib import messages
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
from django.utils.timezone import now

def home(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Start with optimized queryset
    events = Event.objects.select_related('category').only('id', 'name', 'category', 'date')

    # Apply filters
    if query:
        events = events.filter(name__icontains=query)

    if category_filter:
        events = events.filter(category_id=category_filter)

    if start_date and end_date:
        events = events.filter(date__range=[parse_date(start_date), parse_date(end_date)])

    # Optimize for many-to-many relationships
    events = events.prefetch_related('participants')

    categories = Category.objects.only('id', 'name')  # Optimize category query

    return render(request, 'events/home.html', {
        'events': events,
        'categories': categories,
        'query': query,
        'category_filter': category_filter,
        'start_date': start_date,
        'end_date': end_date
    })

def organizer_dashboard(request):
    today = now().date()

    # Optimize queries by prefetching related participants count
    events = Event.objects.prefetch_related('participants').annotate(participant_count=Count('participants'))

    # Optimize total participant count using aggregation (Avoid duplicate count in annotation)
    total_participants = Event.objects.annotate(num_participants=Count('participants')).aggregate(total_sum=Count('participants'))['total_sum']

    # Optimize event counts using filtered aggregations
    event_counts = Event.objects.aggregate(
        total=Count('id'),
        upcoming=Count('id', filter=Q(date__gte=today)),
        past=Count('id', filter=Q(date__lt=today))
    )

    # Get today's events efficiently
    todays_events = events.filter(date=today)

    # Handle event filtering (Re-use the queryset)
    filter_type = request.GET.get('filter', 'all')
    if filter_type == "upcoming":
        filtered_events = events.filter(date__gte=today)
    elif filter_type == "past":
        filtered_events = events.filter(date__lt=today)
    else:
        filtered_events = events

    return render(request, 'events/dashboard.html', {
        'total_participants': total_participants,
        'total_events': event_counts['total'],
        'upcoming_events': event_counts['upcoming'],
        'past_events': event_counts['past'],
        'todays_events': todays_events,
        'events': filtered_events,
        'filter_type': filter_type
    })

# Event Views
def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('participants') \
                          .annotate(participant_count=Count('participants'))

    return render(request, 'events/event_list.html', {'events': events})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

def event_detail(request, pk):
    event = get_object_or_404(Event.objects.prefetch_related('participants'), pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

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

# Participant Views
def participant_list(request):
    participants = Participant.objects.prefetch_related('events').only('name', 'email')
    return render(request, 'participants/participant_list.html', {'participants': participants})


def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'participants/participant_form.html', {'form': form})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participants/participant_form.html', {'form': form})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participants/participant_confirm_delete.html', {'participant': participant})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'categories/category_confirm_delete.html', {'category': category})