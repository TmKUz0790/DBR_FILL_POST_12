# sales/models.py

from django.db import models

class SaleEntry(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='сум')
    total = models.DecimalField(max_digits=15, decimal_places=2)
    dostavka = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')])
    car_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} - {self.total}"
