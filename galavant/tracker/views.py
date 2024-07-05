from django.shortcuts import render
from django.http import HttpResponse
from tracker.models import Location
import googlemaps

# Create your views here.
def location_list(request):
    locations = Location.objects.all()
    print(locations)
    return render(request, 'location/templates/list.html', {'locations': locations})

'''
def location_detail(request, location_name):
    location =
    return render(request, '.html')
'''

'''
def location_lookup(request, search_text):
    #google maps api request

    return render(request,


'''
