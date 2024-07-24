from django.urls import path
from tracker import views
from tracker.views import default_loggedin, trip_list
#from allauth.account.views import LoginView, LogoutView, SignupView


urlpatterns = [
    path("", views.default_loggedin, name="default_loggedin"),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    #path("index/", views.index, name="index"),
    #path("autocomplete/", views.autocomplete, name="autocomplete"),
    #path("store/", views.store_place, name="store_place"),
    #path("gmaps_api_metaai/", views.get_place_details, name="get_place_details"),
    #path("gmaps_api/", views.get_place_details, name="get_place_details"),
    #path("", HomeView.as_view(), name='my_home_view'),
    #path('geocoding/<int:pk>', GeocodingView.as_view(), name = 'my_geocoding_view'),
    path('locationlist/', views.location_list, name='location_list'),
    path('triplist/', views.trip_list, name='trip_list'),
    path('createlocation/', views.create_location, name='create_location'),
    path('createtrip/', views.create_trip, name='create_trip'),
    path('search/', views.search_location, name='search_location')

    
]
