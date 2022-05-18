from django.contrib.auth.models import User, Group
from . import models
from rest_framework import serializers


class RentalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Rental
        fields = ['name','id']

class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ['name','rental_name','checkin_date','checkout_date','previous_reservation','id']