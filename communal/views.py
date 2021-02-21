from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from communal.models.models import Record, UtilityMeter
from communal.serializers import UtilityMeterSerializer, RecordSerializer


@api_view(['POST'])
def set_utility_meter_values(request):

    meters_list = request.user.customer.utility_meters.all()

    serializer = UtilityMeterSerializer(data=request.data)
    serializer.is_valid()
    current_meter = meters_list.get(type=serializer.data['type'])

    serializer_record = RecordSerializer(data=request.data)

    if serializer_record.is_valid(raise_exception=True):
        serializer_record.validated_data['utility_meter'] = current_meter

        print(serializer_record.validated_data)

        if Record.objects.filter(utility_meter=current_meter).exists():
            if serializer_record.validated_data['value'] < Record.objects.filter(utility_meter=current_meter).first().value:
                raise ValidationError('ТЫ КУДА ВОДУ СКРУТИЛ')

        print(serializer_record.validated_data)
        serializer_record.save()

    return Response(serializer_record.data)


@api_view(['GET'])
def utility_meter_history(request):

    meters_list = request.user.customer.utility_meters.all()
    data = []

    for meter in meters_list:
        data += meter.records.all()

    print(data)

    serializer = RecordSerializer(many=True, data=data)

    serializer.is_valid()

    return Response(serializer.data)


@api_view(['GET'])
def debtors(request):

    query = request.query_params

    month = query['month']
    year = query['year']

    um = UtilityMeter.objects.all()

    data = []

    for item in um:
        if not item.records.filter(date__year=year, date__month=month).exists():
            data.append(item)
            print(item)
            print(um)

    print(data)

    serializer = UtilityMeterSerializer(many=True, data=data)

    serializer.is_valid()

    return Response(serializer.data)
