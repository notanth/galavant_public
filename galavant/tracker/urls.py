from django.urls import path
from tracker import views
from tracker.views import default_loggedin


urlpatterns = [
    path('', default_loggedin),
    path("", views.default_loggedin, name="default_loggedin"),
    #path("", HomeView.as_view(), name='my_home_view'),
    #path('geocoding/<int:pk>', GeocodingView.as_view(), name = 'my_geocoding_view'),
    path('locationlist/', views.location_list, name='location_list'),
    path('triplist/', views.trip_list, name='location_list'),
    path('createlocation/', views.create_location, name='create_location'),
    path('createtrip/', views.create_trip, name='create_trip'),

    
]
