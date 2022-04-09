from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('venue-data/<int:venue_index>/', views.venue_data, name='venue-data'),
]