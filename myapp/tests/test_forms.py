import pytest
from mixer.backend.django import mixer
from myapp.forms import RentalForm,ReservationForm

pytestmark = pytest.mark.django_db

# test rental form
class TestRentalForm:
    def test_rentalform(self):
        form = RentalForm()
        assert False is form.is_valid()

        data = {"name": "Hans"}
        form = RentalForm(data=data)
        assert True is form.is_valid()
