import datetime
import uuid

from django.contrib.auth.models import User
from rest_framework import serializers

from communal.models.choices import UtilityMeterType
from communal.models.common import BaseModel
from communal.models.models import UtilityMeter, Record, Customer
from communal.service import validate_utility_meter_data, validate_create_meter, validate_create_record, \
    get_current_meter


class BaseModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4, read_only=True)

    class Meta:
        abstract = True
        model = BaseModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CustomerSerializer(BaseModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['user'] = UserSerializer(instance=instance.user).data
        return data


class RecordSerializer(BaseModelSerializer):
    delta = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Record
        fields = '__all__'
        extra_kwargs = {
            'utility_meter': {'required': False},
            'date': {'required': False},
        }

    def create(self, validated_data):
        data = self.initial_data()
        user = self.context['user']

        current_meter = get_current_meter(data, user)

        validated_data['utility_meter'] = current_meter
        validated_data['date'] = datetime.date.today()

        validate_utility_meter_data(validated_data, current_meter)

        return super(RecordSerializer, self).create(validated_data=validated_data)


class UtilityMeterSerializer(BaseModelSerializer):
    type = serializers.ChoiceField(choices=UtilityMeterType.choices)

    class Meta:
        model = UtilityMeter
        fields = '__all__'
        extra_kwargs = {
            'customer': {'required': False},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)

        # https://stackoverflow.com/questions/30203652/how-to-get-request-user-in-django-rest-framework-serializer
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user

        try:
            data['customer'] = CustomerSerializer(instance=instance.customer).data
        except AttributeError:
            data['customer'] = CustomerSerializer(instance=user).data

        return data

    def create(self, validated_data):
        data = self.initial_data()

        customer, utility_type = validate_create_meter(validated_data, data)

        return UtilityMeter.objects.create(customer=customer, type=utility_type)

