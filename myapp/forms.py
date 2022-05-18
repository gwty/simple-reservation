from django import forms

from myapp.models import Reservation,Rental

class DateInput(forms.DateInput):
    input_type = 'date'

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['rental_name','checkin_date','checkout_date']
        widgets = {
          'rental_name': forms.Textarea(attrs={'rows':1, 'cols':40}),
          'checkin_date':  DateInput(),
          'checkout_date':  DateInput()
        }


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['name']
        widgets = {
          'name': forms.Textarea(attrs={'rows':1, 'cols':40}),
        }
