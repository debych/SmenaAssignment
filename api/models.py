from django.db import models


# Create your models here.

class Printer(models.Model):
    CHECK_TYPES = [
        ('kitchen', 'for kitchen'),
        ('client', 'for client')
    ]

    name = models.CharField(max_length=64, verbose_name="Printer's name")
    api_key = models.CharField(max_length=64, verbose_name="Printer's API key")
    check_type = models.CharField(max_length=32, choices=CHECK_TYPES, verbose_name="Type of printed checks")
    point_id = models.IntegerField(verbose_name="ID of the printer's point")

    def __str__(self):
        return self.name


class Check(models.Model):
    CHECK_TYPES = [
        ('kitchen', 'for kitchen'),
        ('client', 'for client')
    ]
    CHECK_STATUS = [
        ('new', 'new'),
        ('rendered', 'rendered'),
        ('printed', 'printed'),
    ]

    printer = models.ForeignKey('Printer', on_delete=models.CASCADE, verbose_name='Printer that check belongs to')
    type = models.CharField(max_length=32, choices=CHECK_TYPES, verbose_name='Check type')
    order = models.JSONField(verbose_name='Order')
    status = models.CharField(max_length=32, choices=CHECK_STATUS, default='new', verbose_name='Check status')
    pdf_file = models.FileField(null=True, upload_to='pdf/')
