from django.contrib import admin

from communal.models.models import Customer, UtilityMeter, Record

admin.site.register(Customer)
admin.site.register(UtilityMeter)
admin.site.register(Record)
