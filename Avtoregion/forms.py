# -*- coding:utf-8 -*-

from django.forms import ModelForm, DateField
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import SelectDateWidget
from .models import *

MONTHS = {
    1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr',
    5: 'may', 6: 'jun', 7: 'jul', 8: 'aug',
    9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'
}


class TrailerForm(ModelForm):
    class Meta:
        model = Trailer
        fields = ['number']


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['number', 'pts', 'trailer']


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ['name']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name']


class ShipmentForm(ModelForm):
    class Meta:
        model = Shipment
        fields = ['name']


class MediatorForm(ModelForm):
    class Meta:
        model = Mediator
        fields = ['address']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name']


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['name']


class RaceForm(ModelForm):
    race_date = DateField(widget=AdminDateWidget(), label='Дата рейса:')

    class Meta:
        model = Race
        fields = '__all__'
        fields = ['name_race', 'race_date', 'car', 'driver', 'type_ship', 'supplier', 'customer', 'shipment',
                  'mediator', 's_milage', 'e_milage', 'weight_load', 'weight_unload', 'comm', 'state']
        labels = {
                  'car': 'Машина',
                  'driver': 'Водитель',
                  'type_ship': 'Реализация',}
