from django.urls import path

from communal.views import utility_meter_history, set_utility_meter_values, debtors, create_utility_meter

urlpatterns = [
    path('', set_utility_meter_values, name='set_values'),
    path('history/', utility_meter_history, name='history'),
    path('debtors/', debtors, name='debtors'),
    path('create/', create_utility_meter, name='create_meter'),
]