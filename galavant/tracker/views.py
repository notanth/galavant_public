from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from tracker.models import Location, Trip
from tracker.forms import LocationCreateForm, TripCreateForm
from django.views.generic import ListView
from django.views import View
from datetime import datetime
from decouple import config
import googlemaps
import requests
import stripe

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def default_loggedin(request):
    return render(request, 'default_loggedin.html')

def pricing_page_view(request):
    return render(request, 'stripe_subscribe.html')

def location_list(request):
    locations = Location.objects.all()
    print(locations)
    return render(request, 'locationlist_all.html', {'locations': locations})


def trip_list(request):
    trips = Trip.objects.all()
    print(trips)
    return render(request, 'triplist.html', {'trips': trips})

# only created to allow manual input to db from form, will be deprecated
def create_location(request):
    if request.POST:
        form = LocationCreateForm(request.POST)
        print()
        if form.is_valid():
            #place_name = form.cleaned_data['place_name']
            form.save()
            form = LocationCreateForm()
    else:
        form = LocationCreateForm()
    return render(request, 'createlocation.html', {'form': form})


def create_trip(request):
    if request.POST:
        form = TripCreateForm(request.POST)
        print()
        if form.is_valid():
            #place_name = form.cleaned_data['place_name']
            form.save()
            form = TripCreateForm()
    else:
        form = TripCreateForm()
    return render(request, 'createtrip.html', {'form': form})


def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

def search_location_initial(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        api_key = config('GOOGLE_API_KEY')
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={location}&inputtype=textquery&fields=geometry,formatted_address,name,place_id&key={api_key}'
        response = requests.get(url)
        data = response.json()
        print(data)
        if data['status'] == 'OK':
            result = data['candidates'][0]
            return redirect('save_location_preview', 
                            latitude=result['geometry']['location']['lat'], 
                            longitude=result['geometry']['location']['lng'], 
                            city=result['formatted_address'].split(',')[1].strip(), 
                            country=result['formatted_address'].split(',')[-1].strip(), 
                            place_name=result['name'], 
                            place_id=result['place_id'])
        else:
            return render(request, 'search_initial.html', {
                'error': 'Failed to retrieve location info. Please try again.',
            })
    return render(request, 'search_initial.html')

def save_location_preview(request, latitude, longitude, city, country, place_name, place_id):
    return render(request, 'save_location_preview.html', {
        'latitude': latitude,
        'longitude': longitude,
        'city': city,
        'country': country,
        'place_name': place_name,
        'place_id': place_id,
    })

def save_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        city = request.POST.get('city')
        country = request.POST.get('country')
        place_name = request.POST.get('place_name')
        place_id = request.POST.get('place_id')

        location = Location(
            latitude=latitude,
            longitude=longitude,
            city=city,
            country=country,
            place_name=place_name,
            place_id=place_id
        )
        location.save()

        return redirect('location_saved')
    return redirect('search_location')

def location_saved(request):
    return render(request, 'location_saved.html')


'''
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
'''



'''
def location_detail(request, location_name):
    location =
    return render(request, '.html')
'''


'''
def index(request):
    return render(request, "index.html", {"api_key": config('GOOGLE_API_KEY')})

def autocomplete(request):
    # This endpoint can be used for custom logic if needed
    return JsonResponse([], safe=False)


def store_place(request):
    place_id = request.POST.get("place_id")
    place_details = get_place_details(place_id)

    if place_details:
        place_name = place_details.get("name")
        place_lat = place_details["geometry"]["location"]["lat"]
        place_lng = place_details["geometry"]["location"]["lng"]

        print(f"Storing Place ID: {place_id}")
        print(f"Place Name: {place_name}")
        print(f"Latitude: {place_lat}")
        print(f"Longitude: {place_lng}")

        return JsonResponse(
            {
                "place_id": place_id,
                "name": place_name,
                "latitude": place_lat,
                "longitude": place_lng,
            }
        )

    return JsonResponse({}, status=204)


def get_place_details(place_id: str) -> dict:
    url = (
        "https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={place_id}&key={config('GOOGLE_API_KEY')}"
    )
    response = requests.get(url)
    response.raise_for_status()
    result = response.json().get("result")
    return result
'''