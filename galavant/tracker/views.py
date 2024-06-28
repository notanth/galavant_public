from django.shortcuts import render
from tracker.models import Location

# Create your views here.
def location_list(request):
    locations = Location.objects.all()

    return render(request, 'location/list.html', {'locations': locations})


# def location_detail(request, location_name):
    #location = 

    #return render(request, '.html')