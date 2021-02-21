import uuid

from django.contrib.auth.models import User
from rest_framework import serializers

from communal.models.choices import UtilityMeterType
from communal.models.common import BaseModel
from communal.models.models import UtilityMeter, Record, Customer


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

    delta = serializers.IntegerField(required=False)

    class Meta:
        model = Record
        fields = '__all__'
        extra_kwargs = {
            'utility_meter': {'required': False},
            'delta': {'required': False, 'read-only': True},
        }


class UtilityMeterSerializer(BaseModelSerializer):

    type = serializers.ChoiceField(choices=UtilityMeterType.choices)

    class Meta:
        model = UtilityMeter
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['customer'] = CustomerSerializer(instance=instance.customer).data

        return data
