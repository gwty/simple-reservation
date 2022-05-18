# Simple Reservation system

## Project uses
Django
Pytest
REST Framework
Datatables

## To install requirements:
pip3 install -r testing-requirements.txt

## To test:
pytest

## To get coverage:
pytest --cov=. 

## To generate coverage report:
pytest --cov=. --cov-report=html

## To run initial database creation:
python3 manage.py migrate myapp

## To start server:
python3 manage.py runserver

You have to create a rental before creating a reservation in that rental name.

## Create rental:
http://localhost:8000/createrental

## Create reservation:
http://localhost:8000/createreservation/

## Reservation API:
http://localhost:8000/reservations/

## Rental API:
http://localhost:8000/rentals/


# Resources
This project was forked from (https://codecov.io/gh/ptrstn/django-testing-examples)
The Django Test Driven Development Cookbook:
- https://www.youtube.com/watch?v=41ek3VNx_6Q
