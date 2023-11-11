from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('my_locations/', views.my_locations, name='my_locations'),
    path('add_location/', views.add_location, name='add_location'),
    path('location_view/<str:name>', views.location_view, name='location_view'),
    path('delete_location/<str:name>', views.delete_location, name='delete_location'),
]