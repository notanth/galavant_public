from django.urls import path
from tracker import views
from tracker.views import index


urlpatterns = [
    path('', index),
    path('locations', views.location_list, name='location_list'),
    path('create/', views.create_location, name='create_location'),
]
