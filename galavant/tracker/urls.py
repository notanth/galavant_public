from django.urls import path
from tracker import views

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
    path('createtrip/', views.create_trip, name='create_trip'),
    path('search_location/', views.search_location, name='search_location'),
    path('search_location/<str:location>/', views.search_location, name='search_location'),
    path('save_location/', views.save_location, name='save_location'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),

    # assume one of these needs to go or be re-named; one may be poorly named to be user in locationuser table
    path('location_saved/', views.location_saved, name='location_saved'),
    path('save_location/', views.save_location, name='save_location'),

    path('my_locations/', views.location_user_list, name='location_user_list'),
    # path('locationlist/', views.location_list, name='location_list'),

    # for htmx to update user-location; re-visit and re-do/fix



    path('subscribe/', views.pricing_page_view, name='pricing_page_view'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile-updated/', views.profile_updated, name='profile_updated'),



    path('map_pinned/', views.plot_locations, name='plot_locations'),
    path('heatmap/', views.plot_heatmap, name='plot_heatmap'),
    path('mylocationsmapped/', views.my_locations_plot, name='my_locations_plot'),

    # htmx views to update location user
    #path('my_locations/<pk>/update/', views.location_user_update, name='location_user_update'),
    #path('my_locations/<pk>/edit/', views.location_user_edit, name='location_user_edit'),

    path('location_list/', views.location_list, name='location_list'),
    path('edit_location_user/<pk>/', views.edit_location_user, name='edit_location_user'),
    path('delete_location_user/<pk>/', views.delete_location_user, name='delete_location_user'),

    path('edit/<int:pk>/', views.location_edit, name='location_edit'),
    path('update/<int:pk>/', views.location_update, name='location_update'),
    path('delete/<int:pk>/', views.location_delete, name='location_delete'),
]
