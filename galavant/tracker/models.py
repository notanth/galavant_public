from django.db import models
from django.contrib.auth.models import User

# for visualization purposes only ***
'''
class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)
    username = CharField(_("Username"), blank=True, max_length=255)
    email = EmailField(_("Email"), blank=True, max_length=255)
    password = CharField(_("Password"), blank=True, max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
'''



class Trip(models.Model):
    trip_name = models.CharField(max_length=50)
    #username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.trip_name

'''
class Comment(models.Model):
    comment_text = models.TextField()
    place_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = [['traveler', 'place_id']]
    
    def __str__(self):
        return self.comment_text
'''

'''
class LocationProfile(models.Model):
    #location_name = models.CharField(max_length=50, blank=False)
    #user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    place_id = models.ForeignKey("Location", on_delete=models.CASCADE, default=1)
    trip_id = models.ForeignKey("Trip", blank=True, on_delete=models.CASCADE)
    been_to_before = models.BooleanField(default=False, blank=True)
    #comment = models.ForeignKey('Comment', null=True, blank=True)

'''


'''
class Meta:
    unique_together = [['place_id', 'trip_id']]

'''


class Location(models.Model):
    latitude = models.DecimalField(max_digits=12, decimal_places=9,
                                   blank=False)
    longitude = models.DecimalField(max_digits=12, decimal_places=9,
                                    blank=False)
    place_id = models.CharField(max_length=100, blank=False, default=1)
    #models.CharField(max_length=100, unique=True, blank=False, default=)  #this is from GMaps Places API
    place_name = models.CharField(max_length=100, blank=False, default='needs updated')  #Google Maps long_name
    country = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)  # when place first added; for use later
    date_updated = models.DateField(auto_now=True)  #important for process to confirm place ID annually

    # counts
    # total_location_saves = models.PositiveIntegerField(default=0); possible to also do an aggregation table?

    def __str__(self):
        return self.place_name  #change to place long_name


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
