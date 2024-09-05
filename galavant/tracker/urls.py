from django.urls import path
from tracker import views

urlpatterns = [
    path("", views.default_loggedin, name="default_loggedin"),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

  # URLs for profile and subscriptions
    path('subscribe/', views.pricing_page_view, name='pricing_page_view'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile-updated/', views.profile_updated, name='profile_updated'),

    # trip table URLs
    path('triplist/', views.trip_list, name='trip_list'),
    path('createtrip/', views.create_trip, name='create_trip'),

    # location search and save related URLs
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('search_location/', views.search_location, name='search_location'),
    path('search_location/<str:location>/', views.search_location, name='search_location'),
    path('save_location/', views.save_location, name='save_location'),
    path('location_saved/', views.location_saved, name='location_saved'),

    # mapping related URLs
    path('map_pinned/', views.plot_locations, name='plot_locations'),
    path('heatmap/', views.plot_heatmap, name='plot_heatmap'),
    path('mylocationsmapped/', views.my_locations_plot, name='my_locations_plot'),

    # view & URL Bob updated for LOCATION list; edit the LOCATION table directly - NOT LOCATION USER
    path('location_list/', views.location_list, name='location_list'),
    # bob URLs w/ views to update LOCATION - create new/update old LOCATION-USER views based on these examples
    path('edit/<int:pk>/', views.location_edit, name='location_edit'),
    path('update/<int:pk>/', views.location_update, name='location_update'),
    path('delete/<int:pk>/', views.location_delete, name='location_delete'),


    # this is path for a user to see their locations listed - only theirs; view: location_user_list is list of user's locations
    # see above section to make changes
    path('my_locations/', views.location_user_list, name='location_user_list'),
    # path('locationlist/', views.location_list, name='location_list'),
    path('edit_location_user/<pk>/', views.edit_location_user, name='edit_location_user'),
    path('update_location_user/<pk>/', views.update_location_user, name='update_location_user'),
    path('delete_location_user/<pk>/', views.delete_location_user, name='delete_location_user'),

]