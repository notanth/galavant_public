from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from tracker.models import Location, Trip, LocationUser
from tracker.forms import LocationCreateForm, TripCreateForm, ProfileUpdateForm, UserUpdateForm
from django.views.generic import ListView
from django.views import View
from datetime import datetime
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import googlemaps
import requests
import stripe
import folium
from folium.plugins import HeatMap
from dataclasses import dataclass

#create constants for api_key & others?
api_key = config('GOOGLE_API_KEY')


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

@login_required
def location_list(request):
    locations = Location.objects.all()
    print(locations)
    return render(request, 'locationlist_all.html', {'locations': locations})


@login_required
def trip_list(request):
    if request.user.is_authenticated:
        trips = Trip.objects.filter(user=request.user)
    else:
        None
    print(trips)
    return render(request, 'triplist.html', {'trips': trips})

# only created to allow manual input to db from form, will be deprecated
@login_required
def create_location(request):
    if request.POST:
        form = LocationCreateForm(request.POST)
        print()
        if form.is_valid():
            form.save()
            form = LocationCreateForm()
    else:
        form = LocationCreateForm()
    return render(request, 'createlocation.html', {'form': form})

@login_required
def create_trip(request):
    if request.method == 'POST':
        form = TripCreateForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('trip_list')
        else:
            # Form is not valid, display error message
            pass  # You can add additional logic here if needed
    else:
        form = TripCreateForm(request=request)  # Pass request to form
    return render(request, 'createtrip.html', {'form': form})

#update stripe info upon subscription
@login_required
def update_profile(request):
    user = request.user
    if request.user != user:
        return redirect('home')  # or any other page you want to redirect to

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_updated')  # redirect to a success page
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)
    return render(request, 'update_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def profile_updated(request):
    return render(request, 'profile_updated.html')

'''
#object for storing location info, bad practice to use same name as model?
@dataclass
class LocationDetails:
    latitude: float
    longitude: float
    city: str
    country: str
    place_name: str
    place_id: str

    #create method __post__ init:
        data cleaning and/or creating city and country fields 

def store_location_data(location: LocationDetails):
    latitude=result['geometry']['location']['lat']
'''

def search_location_initial(request):
    if request.method == 'POST':
        #named tuple as object
        location = request.POST.get('location')
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={location}&inputtype=textquery&fields=geometry,formatted_address,name,place_id&key={api_key}'
        response = requests.get(url)
        data = response.json()
        print(data)
        if data['status'] == 'OK':
            result = data['candidates'][0]
            #named tuple or data class object to pass 
            #embed object and remove save_location_preivew
            return render(request, 'save_location_preview.html',
                          {location: LocationDetails})
            # pass in instance of dataclass here
            # location_details = LocationDetails(arg1=..., arg2=..., etc)
            '''
                latitude=result['geometry']['location']['lat'],
                longitude=result['geometry']['location']['lng'],
                city=result['formatted_address'].split(',')[1].strip(),
                country=result['formatted_address'].split(',')[-1].strip(),
                place_name=result['name'],
                place_id=result['place_id'],
                api_key=api_key)
            '''
        else:
            return render(request, 'search_initial.html', {
                'error': 'Failed to retrieve location info. Please try again.',
            })
    return render(request, 'search_initial.html')

def search_location(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={location}&inputtype=textquery&fields=geometry,formatted_address,name,place_id&key={api_key}'
        response = requests.get(url)
        data = response.json()
        print(data)
        if data['status'] == 'OK':
            place_id = data['candidates'][0]['place_id']
            place_details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=address_component&key={api_key}'
            place_details_response = requests.get(place_details_url)
            place_details_data = place_details_response.json()
            result = place_details_data['result']
            #create place object ; render should not do all of this logic
            return render(request, 'search_results.html', {
                'latitude': data['candidates'][0]['geometry']['location']['lat'],
                'longitude': data['candidates'][0]['geometry']['location']['lng'],
                #helper function to de-duplicate or use a method for constructor dunder dunder post init data class
                'city': [component['long_name'] for component in result['address_components'] if 'locality' in component['types']][0] if [component['long_name'] for component in result['address_components'] if 'locality' in component['types']] else None,
                'country': [component['long_name'] for component in result['address_components'] if 'country' in component['types']][0] if [component['long_name'] for component in result['address_components'] if 'country' in component['types']] else None,
                'place_name': data['candidates'][0]['name'],
                'place_id': place_id,
                'api_key': api_key,
            })
        else:
            return render(request, 'search_location.html', {
                'error': 'Failed to retrieve location info. Please try again.',
            })
    return render(request, 'search_location.html')

"""
<tr><td><a href...>location</a></td></tr>
from django.urls import reverse
reserve("search_location")
reserve("search_location") + "?location=" + location
"""

@csrf_exempt
@require_POST
def autocomplete(request):
    print(request.POST)
    input_val = request.POST.get('location', '')
    url = f'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input_val}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    #print(data)
    location_options = []
    for location in data['predictions']:
        location_options.append(location['description'])
    print(location_options)
    print(len(location_options))
    location_html_table = """
            <tr>
                <th>Location Options</th>
            </tr>
            {}
    """
    #django function to create url for links 
    #from django.urls import reverse (name of link in urls.py)
    """bites/models.py
        from django.urls import reverse
        tips_link = reverse('tips')
        search_location/
        """
    
    rows = ""
    for location in location_options:
        rows += """
        
            <tr>
                <td><a href='/search_results'</a>></td>
            </tr>
        """.format(location, location)

    location_html_table = location_html_table.format(rows)

    # todo: parse and make table rows table row and table cell; add column with ajax action to handle the checkbox
    # table cell with a link to save to pass that along
    #return render(request, 'location_table_partial.html', {'location_html_table': location_html_table})
    return HttpResponse(location_html_table, content_type='text/plain')

#merge arguments to one object
'''
def save_location_preview(request, latitude, longitude, city, country, place_name, place_id, api_key):
    return render(request, 'save_location_preview.html', {
        'latitude': latitude,
        'longitude': longitude,
        'city': city,
        'country': country,
        'place_name': place_name,
        'place_id': place_id,
        'api_key': api_key,
    })
'''


#check if location exists, update count if it does; if not, create location
#create location user object when save_location
def save_location(request):
    print(request.POST)
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        city = request.POST.get('city')
        country = request.POST.get('country')
        place_name = request.POST.get('place_name')
        place_id = request.POST.get('place_id')

        #get or create is working but +=1 if exists is not. need to investigate
        instance, created = Location.objects.get_or_create(
            latitude=latitude,
            longitude=longitude,
            city=city,
            country=country,
            place_name=place_name,
            place_id=place_id
        )
        if not created:
            instance.total_location_saves +=1

        LocationUser.objects.get_or_create(
            name=place_name,
            location=instance,
            user=request.user,
        )

        return redirect('location_saved')
    return redirect('search_location')

def location_saved(request):
    return render(request, 'location_saved.html')

# view to update location-traveler trip name




#plotting all locations regardless of user
def plot_locations(request):
    locations = Location.objects.all()
    map = folium.Map(location=[15, 0], zoom_start=2)
    for location in locations:
        folium.Marker(
            [location.latitude, location.longitude],
            tooltip=location.place_name,
            #popup=location.place_name
        ).add_to(map)
    map = map._repr_html_()
    return render(request, 'map_pinned.html', {'map': map})


#heatmap of all locations
def plot_heatmap(request):
    locations = Location.objects.all()
    map = folium.Map(location=[15, 0], zoom_start=2)
    heat_data = [[location.latitude, location.longitude] for location in locations]
    folium.plugins.HeatMap(heat_data, radius=15).add_to(map)
    map = map._repr_html_()
    return render(request, 'heatmap.html', {'map': map})

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
