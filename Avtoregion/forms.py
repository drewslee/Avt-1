# -*- coding:utf-8 -*-

from django.forms import ModelForm, CharField, TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms.widgets import SelectDateWidget, DateTimeInput
from django.forms import DateField, DateTimeField, HiddenInput, ModelChoiceField, ChoiceField
from django.utils import timezone

from .models import *

MONTHS = {
    1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель',
    5: 'май', 6: 'июнь', 7: 'июль', 8: 'август',
    9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'
}


class CustomAuthForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    password = CharField(
        label=("Password"),
        strip=False,
        widget=PasswordInput(attrs={'class': 'form-control'}),
    )


class ConstantForm(ModelForm):
    class Meta:
        model = Constants
        fields = '__all__'
        labels = {'organization_unit_full': 'Название организации полностью',
                  'organization_unit_small': 'Короткое название организации',
                  'mechanic': 'Механик', 'dispatcher': 'Дистпечер', 'ogrn': 'ОГРН', 'address': 'Адрес организации'}


class TrailerForm(ModelForm):
    class Meta:
        model = Trailer
        fields = ['number', 'brand_trailer', 'garage_number_trailer']
        labels = {'number': 'Прицеп', 'brand_trailer': 'Марка', 'garage_number_trailer': 'Гаражный номер'}


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['number', 'pts', 'trailer', 'mediator', 'brand', 'garage_number']
        labels = {'number': 'Номер машины', 'pts': 'ПТС', 'trailer': 'Прицеп', 'mediator': 'Посредник',
                  'brand': 'Марка', 'garage_number': 'Гаражный номер'}


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'inn', 'address']
        labels = {'name': 'Поставщик', 'inn': 'ИНН', 'address': 'Адрес организации'}


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', ]
        labels = {'name': 'Название', 'fraction': 'Фракция', }


class ShipmentForm(ModelForm):
    class Meta:
        model = Shipment
        widgets = {
            'customer': HiddenInput
        }
        fields = ['name', 'customer']
        labels = {'name': 'Место разгрузки'}


class LoadForm(ModelForm):
    class Meta:
        model = LoadingPlace
        widgets = {
            'supplier': HiddenInput
        }
        fields = ['address', 'supplier']
        labels = {'address': 'Место погрузки'}


class MediatorForm(ModelForm):
    class Meta:
        model = Mediator
        fields = ['name', 'address', 'inn', ]
        labels = {'address': 'Адрес организации', 'inn': 'ИНН', 'name': 'Название организации'}


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'inn', 'address']
        labels = {'name': 'Клиент', 'inn': 'ИНН', 'address': 'Адрес организации'}


class UnitsForm(ModelForm):
    class Meta:
        model = Units
        fields = ['name', 'short_name']
        labels = {'name': 'Название', 'short_name': 'Короткое название'}


class DriverForm(ModelForm):
    date_med = DateField(widget=SelectDateWidget(), label='Дата мед. освидетельствования:')

    class Meta:
        model = Driver
        fields = ['name', 'group', 'personnel_number', 'driver_card', 'date_med']
        labels = {'name': 'Водитель:', 'group': 'Группа', 'personnel_number': 'Табельный номер',
                  'driver_card': 'Удостоверение'}


class RaceForm(ModelForm):
    race_date = DateTimeField(initial=timezone.now,
                              label='Дата выезда:',
                              widget=DateTimeInput(attrs={'autofocus': ''})
                              )
    arrival_time = DateTimeField(initial=timezone.now,
                                 label='Дата приезда:'
                                 )
    unit_load = ModelChoiceField(queryset=Units.objects.filter(has_deleted=False),
                                 initial='т.',
                                 label='Ед. изм. загружено')
    unit_unload = ModelChoiceField(queryset=Units.objects.filter(has_deleted=False),
                                   initial='т.',
                                   label='Ед. изм. выгружено')
    supplier = ModelChoiceField(queryset=Supplier.objects.filter(has_deleted=False), label='Поставщик')
    customer = ModelChoiceField(queryset=Customer.objects.filter(has_deleted=False), label='Клиент')
    mediator = ModelChoiceField(queryset=Mediator.objects.filter(has_deleted=False), label='Посредник')
    product = ModelChoiceField(queryset=Product.objects.filter(has_deleted=False), label='Груз')
    driver = ModelChoiceField(queryset=Driver.objects.filter(has_deleted=False), label='Водитель')
    car = ModelChoiceField(queryset=Car.objects.filter(has_deleted=False), label='Машина')

    class Meta:
        model = Race
        fields = '__all__'
        labels = {
            'type_ship': 'Реализация',
            'order_type_race': 'Заказчик',
            'place_load': 'Место погрузки',
            'shipment': 'Место разгрузки',
            'product': 'Груз',
            's_milage': 'Начало трeка',
            'e_milage': 'Конец трeка',
            'weight_unload': 'Разгружено',
            'weight_load': 'Загружено',
            'shoulder': 'Плечо',
            'comm': 'Комментарий',
            'state': 'Состояние',
            'gas_given': 'Горючего выдано на рейс',
            'gas_start': 'Горючего остаток на начало рейса',
            'gas_end': 'Горючего остаток на конец рейса',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place_load'].queryset = LoadingPlace.objects.none()
        self.fields['shipment'].queryset = Shipment.objects.none()

        if 'supplier' in self.data:
            try:
                supplier_id = int(self.data.get('supplier'))
                self.fields['place_load'].queryset = LoadingPlace.objects.filter(supplier_id=supplier_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['place_load'].queryset = self.instance.supplier.loadingplace_set

        if 'customer' in self.data:
            try:
                customer_id = int(self.data.get('customer'))
                self.fields['shipment'].queryset = Shipment.objects.filter(customer_id=customer_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['shipment'].queryset = self.instance.customer.shipment_set
