import pytest
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from myapp import views
from myapp.forms import ReservationForm,RentalForm
from myapp.models import Reservation,Rental
import json
pytestmark = pytest.mark.django_db
factory = APIRequestFactory()

class TestRentalView:
    # create rental
    def test_createrental(self):
        assert False is Rental.objects.all().exists()
        data = {
            "id": 1,
            "name": "Test_Rental",
        }
        req = factory.post('/rentals',content_type='application/json',
            data=json.dumps(data))
        view = views.RentalViewSet.as_view(
            {'post': 'create'}
        )
        response = view(req).render()
        assert response.status_code == 201
        assert json.loads(response.content) == data


class TestReservationView:
    # create reservation
    def test_createreservation(self):
        assert False is Reservation.objects.all().exists()
        TestRentalView.test_createrental(self)
        assert True is Rental.objects.all().exists()
        rental_name = Rental.objects.get(id=1).name
        res_data = {
            "rental_name": rental_name,
            "checkin_date": "2022-01-01",
            "checkout_date": "2022-01-05",
        }

        res_data2 = {
            "name":"Res-1",
            "id":1,
            "rental_name": "Test_Rental",
            "checkin_date": "2022-01-01",
            "checkout_date": "2022-01-05",
            "previous_reservation":None
        }
        req = factory.post('/reservations',res_data)
        view = views.ReservationViewSet.as_view(
            {'post': 'create'}
        )
        response = view(req).render()
        assert response.status_code == 201
        assert json.loads(response.content) == res_data2

    # test no rental match
    def test_bad_reservation_norental(self):
            assert False is Reservation.objects.all().exists()
            assert False is Rental.objects.all().exists()
            res_data = {
                "rental_name": "Bad_Rental",
                "checkin_date": "2022-01-01",
                "checkout_date": "2022-01-05",
            }
            req = factory.post('/reservations',res_data)
            view = views.ReservationViewSet.as_view(
                {'post': 'create'}
            )
            response = view(req).render()
            assert response.status_code == 500
            assert response.data['detail'] == 'Rental matching query does not exist.'

    # test checkin after checkout
    def test_bad_reservation_badcheckin(self):
            assert False is Reservation.objects.all().exists()
            TestRentalView.test_createrental(self)
            assert True is Rental.objects.all().exists()
            res_data = {
                "rental_name": "Test_Rental",
                "checkin_date": "2022-02-01",
                "checkout_date": "2022-01-05",
            }
            req = factory.post('/reservations',res_data)
            view = views.ReservationViewSet.as_view(
                {'post': 'create'}
            )
            response = view(req).render()
            assert response.status_code == 500
            assert response.data['detail'] == 'Check-in is after checkout!'

    # test overlapping reservation
    def test_bad_reservation_overlapping(self):
            assert False is Reservation.objects.all().exists()
            TestRentalView.test_createrental(self)
            assert True is Rental.objects.all().exists()
            res_data = {
                "rental_name": "Test_Rental",
                "checkin_date": "2022-01-01",
                "checkout_date": "2022-01-05",
            }
            req = factory.post('/reservations',res_data)
            view = views.ReservationViewSet.as_view(
                {'post': 'create'}
            )
            response = view(req).render()
            res_data = {
                "rental_name": "Test_Rental",
                "checkin_date": "2022-01-02",
                "checkout_date": "2022-01-05",
            }
            req = factory.post('/reservations',res_data)
            view = views.ReservationViewSet.as_view(
                {'post': 'create'}
            )
            response = view(req).render() 
            assert response.status_code == 500
            assert response.data['detail'] == 'There is an overlapping reservation'