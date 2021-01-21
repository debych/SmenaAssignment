from django.test import TestCase
from django.core import serializers
from .models import Printer, Check
import requests


# Create your tests here.

class PrinterCheckModelTest(TestCase):
    printer = Printer(name='test', api_key='123tttt', check_type='kitchen', point_id=1)
    printer.save()
    printer.check_set.create(type='kitchen', order={"id": 12312111132,
                                                    "price": 780,
                                                    "items": [{"name": "Вкусная пицца",
                                                               "quantity": 2,
                                                               "unit_price": 250},
                                                              {"name": "Не менее вкусные роллы",
                                                               "quantity": 1,
                                                               "unit_price": 280}],
                                                    "address": "г. Уфа, ул. Ленина, д. 42",
                                                    "client": {"name": "Иван",
                                                               "phone": 9173332222},
                                                    "point_id": 2})
    printer.save()


class CreateCheckApiTest(TestCase):
    printer = Printer(name='test', api_key='123tttt', check_type='kitchen', point_id=1)
    printer.save()
    data = {"id": 12312111132,
            "price": 780,
            "items": [{"name": "Вкусная пицца",
                       "quantity": 2,
                       "unit_price": 250},
                      {"name": "Не менее вкусные роллы",
                       "quantity": 1,
                       "unit_price": 280}],
            "address": "г. Уфа, ул. Ленина, д. 42",
            "client": {"name": "Иван",
                       "phone": 9173332222},
            "point_id": 2}
    r = requests.post('http://localhost/api/create_checks/', json=data)
    print(serializers.serialize('json', Check.objects.all()))
