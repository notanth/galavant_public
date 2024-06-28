from django.contrib import admin
from tracker.models import Location, Traveler

# Register your models here.
@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    list_display = ['username', 'twitter_handle']
    search_field = ['username']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'date_created']
    search_field = ['location_name']