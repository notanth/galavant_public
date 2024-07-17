from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from tracker.models import Location
from tracker.forms import LocationCreateForm
from django.views.generic import ListView
from django.views import View
from datetime import datetime
import googlemaps

# Create your views here.
def index(request):
    return render(request, 'index.html')


def location_list(request):
    locations = Location.objects.all()
    print(locations)
    return render(request, 'list.html', {'locations': locations})


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


def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()


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
def location_lookup(request, search_text):
    #google maps api request

    return render(request,
'''
