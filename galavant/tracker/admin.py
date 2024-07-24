from django.contrib import admin
from tracker.models import Location, Profile, Trip, LocationUser  #Comment #TravelerLocation


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'twitter_handle']
    search_field = ['user']


@admin.register(LocationUser)
class LocationUserAdmin(admin.ModelAdmin):
    list_display = ['location', 'user']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['place_name', 'place_id', 'date_created', 'country', 'city', 'date_updated']
    search_field = ['place_name']



@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['trip_name', 'user']
    search_field = ['trip_name']

'''
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'date_created']
'''
