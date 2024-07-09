from django.urls import path, include
from tracker import views
from tracker.views import index


urlpatterns = [
    path('', views.location_list, name='location_list'),
    path('create/', views.create_location, name='create_location'),
    path('', index)
]
