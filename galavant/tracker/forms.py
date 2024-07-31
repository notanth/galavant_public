from django import forms

from tracker.models import Location


class LocationCreateForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
