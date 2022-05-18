from django.db import models

class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    rental_id = models.ForeignKey(Rental,on_delete=models.CASCADE)
    rental_name = models.TextField()
    name = models.TextField(null=True)
    checkin_date = models.DateField(auto_now=False, auto_now_add=False)
    checkout_date = models.DateField(auto_now=False, auto_now_add=False)
    previous_reservation = models.TextField(null=True)