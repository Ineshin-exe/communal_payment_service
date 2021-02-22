from django.contrib.auth.models import User
from django.db import models

from communal.models.choices import UtilityMeterType
from communal.models.common import BaseModel, SingletonModel


class Manager(SingletonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager')


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    apartment = models.CharField(max_length=8)

    def __str__(self):
        return f"U: {self.user}, Apartment: {self.apartment}"


class UtilityMeter(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='utility_meters')
    type = models.CharField(max_length=32, choices=UtilityMeterType.choices, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'type'], name='customer_type')
        ]

    def __str__(self):
        return f"Apartment: {self.customer.apartment}, Type: {self.type}"


class Record(BaseModel):
    utility_meter = models.ForeignKey(UtilityMeter, on_delete=models.CASCADE, related_name='records')
    date = models.DateField(null=False, blank=False)
    value = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = ['-date']

    @property
    def delta(self):
        return self.value - Record.objects.filter(value__lte=self.value).exclude(id=self.id).first().value

    def __str__(self):
        return f"Meter: {self.utility_meter.__str__()} \n Date: {self.date}, Value: {self.value}"
