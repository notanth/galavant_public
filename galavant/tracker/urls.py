from django.urls import path
from tracker import views
from tracker.views import index


urlpatterns = [
    path('', index),
    #path("", HomeView.as_view(), name='my_home_view'),
    #path('geocoding/<int:pk>', GeocodingView.as_view(), name = 'my_geocoding_view'),
    path('locations', views.location_list, name='location_list'),
    path('createlocation/', views.create_location, name='create_location'),
    
]
