from rest_framework import serializers
from main.models import *


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [field.name for field in Client._meta.get_fields()]


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedData
