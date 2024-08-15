from django import forms
from tracker.models import Location, Trip, LocationUser


class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'

class LocationUserForm(forms.ModelForm):
    class Meta:
        model = LocationUser
        fields = ('name', 'location', 'trip', 'been_to_before')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'trip': forms.Select(attrs={'class': 'form-control'}),
            'been_to_before': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


#class SearchLocationForm():