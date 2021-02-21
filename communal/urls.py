from django.urls import path

from communal.views import utility_meter_history, set_utility_meter_values, debtors

urlpatterns = [
    path('', set_utility_meter_values, name='default'),
    path('history/', utility_meter_history, name='default'),
    path('debtors/', debtors, name='default'),

]