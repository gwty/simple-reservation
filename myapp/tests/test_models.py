import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

# Test Rental model
class TestRental:
    def test_rental(self):
        rental_model = mixer.blend("myapp.Rental")
        assert rental_model.pk == 1, "Should create a Rental instance"

# Test Reservation model
class TestReservation:
    def test_rental(self):
        reservation_model = mixer.blend("myapp.Reservation")
        
        assert reservation_model.pk == 1, "Should create a Reservation instance"