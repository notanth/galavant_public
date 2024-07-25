from django import forms

from tracker.models import Location, Trip


class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'


#class SearchLocationForm():