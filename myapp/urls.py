from django.conf.urls import url
from rest_framework import renderers
from django.urls import path, include
from . import views

rental_list = views.RentalViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
rental_detail = views.RentalViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


reservation_list = views.ReservationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
reservation_detail = views.ReservationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})



app_name = 'myapp'
urlpatterns = [
    url(r'^createreservation/', views.ReservationView.as_view(), name='myview'),
    url(r'^createrental/', views.RentalView.as_view(), name='myview2'),
    url(r'^create/$', views.RentalView.as_view(), name='mycreateview'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.ReservationView.as_view(), name='myupdateview'),
    path('rentals/', rental_list, name='rental-list'),
    path('rentals/<int:pk>/', rental_detail, name='rental-detail'),
    path('reservations/', reservation_list, name='reservation-list'),
    path('reservations/<int:pk>/', reservation_detail, name='reservation-detail'),


]
