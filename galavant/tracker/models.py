from django.contrib.auth.models import User
from django.db import models
from dataclasses import dataclass
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    total_location_saves = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.place_name


@dataclass
class LocationDetails:
    latitude: float
    longitude: float
    city: str
    country: str
    place_name: str
    place_id: str

class LocationUser(models.Model):
    name = models.CharField(max_length=50, blank=False) #if user wants to give a custom name, default to place_name
    #place_id = 
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1) #place_name from google, should we switch to/include place_id?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, blank=True, on_delete=models.CASCADE, null=True)
    been_to_before = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    location_user = models.ForeignKey(LocationUser, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment


# is User auto created? Extend default user model? Allauth directly?
class Profile(models.Model):  # profile table
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True)
    twitter_handle = models.CharField(max_length=25)
    bio = models.TextField(max_length=500, blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    # counts
    places_saved = models.PositiveIntegerField(default=0)
    countries_saved = models.PositiveIntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    def __str__(self):
        return self.username
