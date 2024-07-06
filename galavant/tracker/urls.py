from django.urls import path, include
from tracker import views


urlpatterns = [
    path('', views.location_list, name='location_list'),
    
]
