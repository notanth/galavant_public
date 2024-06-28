from django.db import models

# Create your models here.

# use DateTimeField vs DateField?
# use FloatField vs Decimal field? See Python decimal docs

# intent of this table is to let users create "categories" like spring break 
# so they can use it to group saved places/lite itinerary
'''
class Trips(models.Model):
    trip_name = models.CharField(max_length=50)
    username = models.ForeignKey()
    # try Field.choices here, user to add their own then dropdown from their values?
'''

'''
# secondary table that allows each user to add comments and tags to place ID
class LocationTraveler:
    traveler =
    place_id = models.ForeignKey()
    been_to_before = models.BooleanField(default=False)


    Meta:
        unique together
'''



class Location(models.Model):
    location_name = models.CharField(max_length=50, blank=False) #this may be redundant w place_anme
    latitude = models.DecimalField(max_digits=12, decimal_places=9) #need to find new solution to incorporate direction
    longitude = models.DecimalField(max_digits=12, decimal_places=9) #need to find new solution to incorporate direction
    #place_id #this is from GMaps Places API
    #place_name # assume Maps also has this
    date_created = models.DateTimeField(auto_now_add=True) # when place first added; for use later
    #date_updated = models.DateField(auto_now=True) only relevant at user level
    #been_to = models.BooleanField(default=False) # True/False, designates a place user has already been to

    

    def __str__(self):
        return self.location_name #change to place_name

'''
# alternative to extending default user class? Ability to have friends..?
class User(models.model): PROFILE TABLE
    # interested in SuperTokens for email only sign in option
    # look at allauth and dj-paddle for billing; use one or both?
'''

# is User auto created? Extend default user model? Allauth directly?
class Traveler(models.Model): # profile table
    username = models.CharField(max_length=25, unique=True)
    twitter_handle = models.CharField(max_length=25, unique=True) #profile table
    #email = models.EmailField(max_length=100, unique=True)
    #date_created =
    #last_login = 

    # counts
    #places_saved
    #countries_saved

    #class Meta:
        #ordering = ['-id']

    def __str__(self):
        return self.username
