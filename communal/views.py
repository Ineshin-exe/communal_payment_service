from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from communal.models.models import UtilityMeter
from communal.serializers import UtilityMeterSerializer, RecordSerializer


@api_view(['POST'])
def set_utility_meter_values(request):
    serializer = RecordSerializer(data=request.data)
    serializer.context['user'] = request.user

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def utility_meter_history(request):

    paginator = PageNumberPagination()
    paginator.page_size = 20

    meters_list = request.user.customer.utility_meters.all()
    data = []
    for meter in meters_list:
        data += meter.records.all()

    result_page = paginator.paginate_queryset(data, request)
    serializer = RecordSerializer(data=result_page, many=True)
    serializer.is_valid()

    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def debtors(request):

    paginator = PageNumberPagination()
    paginator.page_size = 20

    month = request.query_params['month']
    year = request.query_params['year']

    meters = UtilityMeter.objects.all().order_by('customer')
    data = []
    for meter in meters:
        if not meter.records.filter(date__year=year, date__month=month).exists():
            data.append(meter)

    result_page = paginator.paginate_queryset(data, request)
    serializer = UtilityMeterSerializer(data=result_page, many=True)
    serializer.is_valid()

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def create_utility_meter(request):
    serializer = UtilityMeterSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)
