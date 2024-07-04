from django.db import models
from django.contrib.auth.models import User


class Trip(models.Model):
    trip_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.trip_name



class Location(models.Model):
    """Cache table for google maps API"""
    latitude = models.DecimalField(max_digits=12, decimal_places=9,
                                   blank=False)
    longitude = models.DecimalField(max_digits=12, decimal_places=9,
                                    blank=False)
    place_id = models.CharField(max_length=100, blank=False, default=1)
    place_name = models.CharField(max_length=100, blank=False, default='needs updated')  #Google Maps long_name
    country = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)  # when place first added; for use later
    date_updated = models.DateField(auto_now=True)  #important for process to confirm place ID annually
    total_location_saves = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.place_name


class LocationUser(models.Model):
    name = models.CharField(max_length=50, blank=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, blank=True, on_delete=models.CASCADE)
    been_to_before = models.BooleanField(default=False, blank=True)


class Comment(models.Model):
    location_user = models.ForeignKey(LocationUser, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment


# is User auto created? Extend default user model? Allauth directly?
class Profile(models.Model):  # profile table
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    twitter_handle = models.CharField(max_length=25, unique=True)

    # counts
    #places_saved
    #countries_saved

    #class Meta:
    #ordering = ['-id']

    def __str__(self):
        return self.username
