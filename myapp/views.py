from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import generic, View
from rest_framework import viewsets
from rest_framework import permissions
from myapp.serializers import RentalSerializer,ReservationSerializer
from myapp import models, forms
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework.exceptions import APIException
from datetime import datetime,timedelta
import requests
from django.urls import resolve


class ReservationView(View):
    model = models.Reservation
    form_class = forms.ReservationForm
    def get(self, request, *args, **kwargs):
        form = forms.ReservationForm()
        context = {'form': form}
        return render(request, 'myapp/reservation.html', context)

class RentalView(View):
    model = models.Rental
    form_class = forms.RentalForm
    def get(self, request, *args, **kwargs):
        form = forms.RentalForm()
        context = {'form': form}
        return render(request, 'myapp/rental.html', context)


class UpdateReservationView(generic.UpdateView):
    model = models.Reservation
    form_class = forms.ReservationForm
    success_url = "/update_success/"

class CreateReservation(generic.CreateView):
    model = models.Reservation
    form_class = forms.ReservationForm
    success_url = "/create_success/"

class CreateRental(generic.CreateView):
    model = models.Rental
    form_class = forms.RentalForm
    success_url = "/create_success/"


class RentalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rentals to be viewed or created.
    """
    queryset = models.Rental.objects.all()
    serializer_class = RentalSerializer

    def perform_create(self, serializer):
        serializer.save()

class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reservations to be viewed or created.
    """
    queryset = models.Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        try:
            checkin_date = self.request.POST.get('checkin_date')
            checkout_date = self.request.POST.get('checkout_date')
            rental_name = self.request.POST.get('rental_name')
        except Exception as e:
            raise APIException('Error getting POST variables ' + str(self.request.POST))
        try:
            rental_id = models.Rental.objects.get(name=rental_name)
            if rental_id is None:
                r = Rental(name=rental_name)
                r.save()
                rental_id = r
                #raise APIException("Rental does not exist!")

            if checkin_date > checkout_date:
                raise APIException("Check-in is after checkout!")
            
            objects = models.Reservation.objects.filter(rental_id=rental_id)
            previous_reservation = None
            if len(objects) > 0:
                previous_reservation = objects
                overlapping_reservation_checkin = objects.filter(checkin_date__range=[checkin_date ,checkout_date])
                if overlapping_reservation_checkin:
                    raise APIException("There is an overlapping reservation")
                overlapping_reservation_checkout = objects.filter(checkout_date__range=[checkin_date ,checkout_date])
                if overlapping_reservation_checkout:
                    raise APIException("There is an overlapping reservation")
                if checkin_date==checkout_date:
                    overlapping_reservation_checkout = objects.filter(checkout_date__range=[checkin_date ,checkin_date])
                    if overlapping_reservation_checkout:
                        raise APIException("There is an overlapping reservation")
                previous_reservation= previous_reservation.order_by('-id')[0]
                previous_reservation = 'Res-' + str(previous_reservation.id)

                    
                
            current_obj = serializer.save(rental_id=rental_id,previous_reservation=previous_reservation)
            current_obj.name = 'Res-' + str(current_obj.id)
            current_obj.save()

        except Exception as e:
            print(e)
            raise APIException(e)
        