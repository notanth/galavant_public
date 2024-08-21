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
    path("autocomplete/", views.autocomplete, name="autocomplete"),
    #path("store/", views.store_place, name="store_place"),
    #path("gmaps_api_metaai/", views.get_place_details, name="get_place_details"),
    #path("gmaps_api/", views.get_place_details, name="get_place_details"),
    #path("", HomeView.as_view(), name='my_home_view'),
    #path('geocoding/<int:pk>', GeocodingView.as_view(), name = 'my_geocoding_view'),
    
    path('triplist/', views.trip_list, name='trip_list'),
    path('createlocation/', views.create_location, name='create_location'),
    path('createtrip/', views.create_trip, name='create_trip'),
    path('search_location/', views.search_location, name='search_location'),
    path('search_location/<str:location>/', views.search_location, name='search_location'),
    path('save_location/', views.save_location, name='save_location'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('location_saved/', views.location_saved, name='location_saved'),

    path('my_locations/', views.location_user_list, name='location_user_list'),
    path('locationlist/', views.location_list, name='location_list'),
    path('edit_location_user/', views.edit_location_user_view, name='edit_location_user_view'),
    path('update_location_user/', views.update_location_user_view, name='update_location_user_view'),
    
    path('save_location/', views.save_location, name='save_location'),


    path('subscribe/', views.pricing_page_view, name='pricing_page_view'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile-updated/', views.profile_updated, name='profile_updated'),
    


    path('map_pinned/', views.plot_locations, name='plot_locations'),
    path('heatmap/', views.plot_heatmap, name='plot_heatmap'),
    path('mylocationsmapped/', views.my_locations_plot, name='my_locations_plot'),
    
    # htmx views to update location user
    path('my_locations/<pk>/update/', views.location_user_update, name='location_user_update'),
    #path('my_locations/<pk>/edit/', views.location_user_edit, name='location_user_edit'),
    
]
