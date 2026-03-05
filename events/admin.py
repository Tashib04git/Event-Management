from django.contrib import admin
from events.models import Event, Participant, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'time', 'location', 'category']
    list_filter = ['category', 'date']
    search_fields = ['name', 'location']
    date_hierarchy = 'date'


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']
    filter_horizontal = ['events']
