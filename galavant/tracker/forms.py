from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from tracker.models import Location, Trip, LocationUser


class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ('trip_name',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TripCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(TripCreateForm, self).save(commit=False)
        instance.user = self.request.user
        if commit:
            instance.save()
        return instance

    def clean_trip_name(self):
        trip_name = self.cleaned_data['trip_name']
        if Trip.objects.filter(user=self.request.user, trip_name=trip_name).exists():
            raise ValidationError('You have already created a trip with this name.')
        return trip_name

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