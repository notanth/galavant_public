from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from tracker.models import Location, Trip, LocationUser, LocationDetails
from tracker.forms import TripCreateForm, ProfileUpdateForm, UserUpdateForm
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests
import folium
from folium.plugins import HeatMap

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

# this shows all locations regardless of user
@login_required
def location_list(request):
    locations = Location.objects.all()
    print(locations)
    return render(request, 'locationlist_all.html', {'locations': locations})

@login_required
def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    return render(request, 'location_edit_partial.html', {'location': location})

@login_required
def location_update(request, pk):
    location = get_object_or_404(Location, pk=pk)
    location.place_name = request.POST.get('place_name', location.place_name)
    location.country = request.POST.get('country', location.country)
    location.city = request.POST.get('city', location.city)
    location.save()
    return render(request, 'location_row_partial.html', {'location': location})

@login_required
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    location.delete()
    return JsonResponse({'success': True})

# trip list specific to logged in user
@login_required
def trip_list(request):
    if request.user.is_authenticated:
        trips = Trip.objects.filter(user=request.user)
    else:
        None
    print(trips)
    return render(request, 'triplist.html', {'trips': trips})

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

@login_required
def search_location(request, location=Location):
    url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={location}&inputtype=textquery&fields=geometry,formatted_address,name,place_id&key={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    if data['status'] == 'OK' and data['candidates']:
        place_id = data['candidates'][0]['place_id']
        print("place id is: ", place_id)
        place_details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=address_component&key={api_key}'
        place_details_response = requests.get(place_details_url)
        place_details_data = place_details_response.json()
        result = place_details_data['result']
        print("result of place details data is: ", result)
        location_details = LocationDetails(
            latitude=data['candidates'][0]['geometry']['location']['lat'],
            longitude=data['candidates'][0]['geometry']['location']['lng'],
            city = next((component['long_name'] for component in result['address_components'] if 'locality' in component['types']), None),
            country = next((component['long_name'] for component in result['address_components'] if 'country' in component['types']), None),
            place_name=data['candidates'][0]['name'],
            place_id=place_id,
        )
        print("location_details for search_results : ", location_details)
        request.session['location_details'] = location_details.__dict__
        return render(request, 'search_results.html', {
            'location_details': location_details,
            'api_key': api_key,
        })
    else:
        return render(request, 'search_location.html', {
            'error': 'No location found. Please try again.',
        })

@csrf_exempt
@require_POST
def autocomplete(request):
    print(request.POST)
    input_val = request.POST.get('location', '')
    url = f'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input_val}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    location_options = []
    for location in data['predictions']:
        #print("Location option:", location)
        location_options.append(location['description'])
    print("Locations_options are: ", location_options)
    location_html_table = """
            <tr>
                <th>Suggested Location Options</th>
            </tr>
            {}
    """
    rows = ""
    for location in location_options:
        search_location_url = reverse('search_location', args=[location])
        rows += """
            <tr>
                <td><a href="{}">{}</a></td>
            </tr>
        """.format(search_location_url, location)

    location_html_table = location_html_table.format(rows)

    return HttpResponse(location_html_table, content_type='text/plain')

    """bites/models.py
        from django.urls import reverse
        tips_link = reverse('tips')
        search_location/
        """

    # todo: parse and make table rows table row and table cell; add column with ajax action to handle the checkbox
    # table cell with a link to save to pass that along
    #return render(request, 'location_table_partial.html', {'location_html_table': location_html_table})


#check if location exists, update count if it does; if not, create location
#create location user object when save_location
@login_required
def save_location(request):
    print("Save location view called")
    if request.method == 'POST':
        print("POST request received")
        location_details = LocationDetails(**request.session.get('location_details', {}))
        print("Location details:", location_details.__dict__)

        # Get or create a Location instance
        instance, created = Location.objects.get_or_create(
            latitude=location_details.latitude,
            longitude=location_details.longitude,
            place_name=location_details.place_name,
            place_id=location_details.place_id,
            defaults={
                'city': location_details.city or '',
                'country': location_details.country or '',
            }
        )
        print("Location instance:", instance.__dict__)
        if not created:
            instance.total_location_saves += 1
            instance.save()
            print("Location instance saved")

        # Create a LocationUser instance
        location_user, created = LocationUser.objects.get_or_create(
            name=location_details.place_name,
            location=instance,
            user=request.user,
        )
        print("LocationUser instance:", location_user.__dict__)

        return redirect('location_saved')
    return redirect('search_location')


@login_required
def location_saved(request):
    locations = Location.objects.all()
    return render(request, 'location_saved.html', {'locations': locations})


#location user list view to be editable
@login_required
def location_user_list(request):
    location_users = LocationUser.objects.filter(user=request.user)
    return render(request, 'locationuser_list.html', {'location_users': location_users})

@csrf_exempt
@login_required
def edit_location_user(request, pk):
    print("Request method:", request.method)
    print("Request body:", request.body)
    location_user = LocationUser.objects.get(pk=pk)
    print("Location user object got from db")
    if location_user.user != request.user:
        return redirect('location_user_list')
    if request.method == 'POST':
        print("POST request confirmed")
        editing = False
        data = request.POST
        print("Data:", data)
        # Update the location_user object with the form data
        location_user.location.country = data.get('country')
        location_user.location.name = data.get('name')
        location_user.location.place_name = data.get('location')
        if location_user.trip is None:
            location_user.trip = Trip(trip_name=data.get('trip'), user=request.user)
        else:
            location_user.trip.trip_name = data.get('trip')
        location_user.been_to_before = data.get('been_to_before')
        print("Saving updated location user object")
        location_user.location.save()
        location_user.trip.save()
        location_user.save()
        return render(request, '_edit_locationuser_row.html', {'location_user': location_user, 'editing': editing})
    else:
        editing = True
        return render(request, '_edit_location_user.html', {'location_user': location_user, 'editing': editing})

@login_required
def update_location_user(request, pk):
    location_user = LocationUser.objects.get(pk=pk)
    if location_user.user != request.user:
        return redirect('location_user_list')
    print("deleting location user ")
    #location_user.delete()
    return redirect('location_user_list')


@login_required
def delete_location_user(request, pk):
    location_user = LocationUser.objects.get(pk=pk)
    if location_user.user != request.user:
        return redirect('location_user_list')
    print("deleting location user ")
    location_user.delete()
    return redirect('location_user_list')


# old view before using meta ai
'''
@login_required
def edit_location_user(request, pk):
    location_users = LocationUser.objects.filter(user=request.user)
    if request.method == 'POST':
        location_user_id = request.GET.get('location_user_id')
        location_user = LocationUser.objects.get(id=location_user_id)
        return render(request, '_edit_locationuser_row.html', {'location_user': location_user})
    else:
        return HttpResponse(status=400)  # Return a bad request response
'''




'''
# should allow for row editing with htmx?
@login_required
def location_user_update(request, pk):
    print("location_user_update activated !")
    location_user = LocationUser.objects.get(pk=pk)
    return render(request, '_locationuser_row.html', {'location_user': location_user})
'''


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

#plot locations only for one user
@login_required
def my_locations_plot(request):
    if request.user.is_authenticated:
        # Get locations associated with the logged-in user
        user_locations = LocationUser.objects.filter(user=request.user)

        # Get location data from the Location model
        locations = Location.objects.filter(id__in=user_locations.values_list('location_id', flat=True))

        # Plot locations
        map = folium.Map(location=[15, 0], zoom_start=2)
        for location in locations:
            folium.Marker(
                [location.latitude, location.longitude],
                tooltip=location.place_name,
                #popup=location.place_name
            ).add_to(map)
        map = map._repr_html_()

        return render(request, 'locationuser_map.html', {'map': map})
    else:
        return redirect('login')  # Redirect to login page if user is not authenticated

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



"""
<tr><td><a href...>location</a></td></tr>
from django.urls import reverse
reserve("search_location")
reserve("search_location") + "?location=" + location
"""

'''
    #create method __post__ init:
        data cleaning and/or creating city and country fields
'''
