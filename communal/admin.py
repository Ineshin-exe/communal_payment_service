from django.contrib import admin

from communal.models.models import Manager, Customer, UtilityMeter, Record

admin.site.register(Manager)
admin.site.register(Customer)
admin.site.register(UtilityMeter)
admin.site.register(Record)
