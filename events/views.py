from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date

from events.models import Event, Participant, Category
from events.forms import EventForm, ParticipantForm, CategoryForm

# DASHBOARD

def dashboard(request):
    today = date.today()
    filter_type = request.GET.get('filter', 'today')

    # Aggregate: total participants across all events
    total_participants = Participant.objects.aggregate(total=Count('id'))['total']
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()

    # Interactive stats: dynamically update list based on filter
    if filter_type == 'upcoming':
        event_list = Event.objects.filter(date__gte=today).select_related('category').prefetch_related('participants')
        section_title = "Upcoming Events"
    elif filter_type == 'past':
        event_list = Event.objects.filter(date__lt=today).select_related('category').prefetch_related('participants')
        section_title = "Past Events"
    elif filter_type == 'all':
        event_list = Event.objects.all().select_related('category').prefetch_related('participants')
        section_title = "All Events"
    else:
        # Default: today's events
        event_list = Event.objects.filter(date=today).select_related('category').prefetch_related('participants')
        section_title = "Today's Events"

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'event_list': event_list,
        'section_title': section_title,
        'filter_type': filter_type,
        'today': today,
    }
    return render(request, 'events/dashboard.html', context)

# EVENTS

def event_list(request):
    # Optimized: select_related for category, prefetch_related for participants
    events = Event.objects.select_related('category').prefetch_related('participants').all()

    # Search by name or location using icontains
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )
    if category_id:
        events = events.filter(category_id=category_id)
    if date_from:
        events = events.filter(date__gte=date_from)
    if date_to:
        events = events.filter(date__lte=date_to)

    # Aggregate : total participants across all events
    total_participants = Participant.objects.aggregate(total=Count('id'))['total']
    categories = Category.objects.all()

    context = {
        'events': events,
        'total_participants': total_participants,
        'search_query': search_query,
        'categories': categories,
        'selected_category': category_id,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    # select_related + prefetch_related for optimized queries
    event = get_object_or_404(
        Event.objects.select_related('category').prefetch_related('participants'),
        pk=pk
    )
    return render(request, 'events/event_detail.html', {'event': event})


def event_create(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" created successfully!')
            return redirect('event_detail', pk=event.pk)
    return render(request, 'events/event_form.html', {
        'form': form, 'title': 'Create Event', 'action': 'Create'
    })


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" updated successfully!')
            return redirect('event_detail', pk=event.pk)
    return render(request, 'events/event_form.html', {
        'form': form, 'title': 'Edit Event', 'action': 'Update', 'event': event
    })


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        name = event.name
        event.delete()
        messages.success(request, f'Event "{name}" deleted successfully!')
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'object': event, 'type': 'Event'})

# PARTICIPANTS

def participant_list(request):
    search = request.GET.get('search', '')
    participants = Participant.objects.prefetch_related('events').all()
    if search:
        participants = participants.filter(
            Q(name__icontains=search) | Q(email__icontains=search)
        )
    return render(request, 'events/participant_list.html', {
        'participants': participants, 'search': search
    })


def participant_detail(request, pk):
    participant = get_object_or_404(
        Participant.objects.prefetch_related('events__category'), pk=pk
    )
    return render(request, 'events/participant_detail.html', {'participant': participant})


def participant_create(request):
    form = ParticipantForm()
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'Participant "{participant.name}" added successfully!')
            return redirect('participant_detail', pk=participant.pk)
    return render(request, 'events/participant_form.html', {
        'form': form, 'title': 'Add Participant', 'action': 'Add'
    })


def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    form = ParticipantForm(instance=participant)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'Participant "{participant.name}" updated!')
            return redirect('participant_detail', pk=participant.pk)
    return render(request, 'events/participant_form.html', {
        'form': form, 'title': 'Edit Participant', 'action': 'Update', 'participant': participant
    })


def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        name = participant.name
        participant.delete()
        messages.success(request, f'Participant "{name}" deleted!')
        return redirect('participant_list')
    return render(request, 'events/confirm_delete.html', {'object': participant, 'type': 'Participant'})

# CATEGORIES

def category_list(request):
    categories = Category.objects.annotate(event_count=Count('events')).all()
    return render(request, 'events/category_list.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    events = Event.objects.filter(category=category).prefetch_related('participants')
    return render(request, 'events/category_detail.html', {
        'category': category, 'events': events
    })


def category_create(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created!')
            return redirect('category_list')
    return render(request, 'events/category_form.html', {
        'form': form, 'title': 'Create Category', 'action': 'Create'
    })


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated!')
            return redirect('category_list')
    return render(request, 'events/category_form.html', {
        'form': form, 'title': 'Edit Category', 'action': 'Update', 'category': category
    })


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted!')
        return redirect('category_list')
    return render(request, 'events/confirm_delete.html', {'object': category, 'type': 'Category'})
