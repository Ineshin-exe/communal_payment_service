from rest_framework.exceptions import ValidationError

from communal.models.models import Record, Customer, UtilityMeter


def validate_utility_meter_data(validated_data, meter):
    if Record.objects.filter(utility_meter=meter).exists():
        _check_less_than_previous(validated_data, meter)
        _check_value_already_exists(validated_data, meter)


def _check_less_than_previous(validated_data, meter):
    if Record.objects.filter(utility_meter=meter, value__gt=validated_data['value']).exists():
        raise ValidationError('ТЫ КУДА ВОДУ СКРУТИЛ?')


def _check_value_already_exists(validated_data, meter):
    date = validated_data['date']

    if Record.objects.filter(utility_meter=meter, date__year=date.year, date__month=date.month).exists():
        raise ValidationError('ТЫ УЖЕ ПОДАЛ')


def get_current_meter(data, user):
    meters = user.customer.utility_meters.all()

    try:
        return meters.get(type=data['type'])
    except UtilityMeter.DoesNotExist:
        raise ValidationError('У вас нет такого счетчика')


def validate_create_meter(validated_data, data):
    utility_type = validated_data.get('type')
    customer = _check_register_customer(data)

    if UtilityMeter.objects.filter(customer=customer, type=utility_type).exists():
        raise ValidationError('Такой счетчик у этого пользователя уже установлен')

    return customer, utility_type


def _check_register_customer(data):
    try:
        return Customer.objects.get(apartment=data.get('apartment'))
    except Customer.DoesNotExist:
        raise ValidationError('Такой пользователь не зарегистрирован')
