from rest_framework import serializers
from app_api.models import (Category, Client, Order, Worksheet)


class CategorySerializerModel(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ClientSerializerModel(serializers.ModelSerializer):

    class Meta:

        model = Client
        fields = '__all__'


class OrderSerializerModel(serializers.ModelSerializer):

    class Meta:

        model = Order
        fields = '__all__'


class AllIfoSerializerModel(serializers.ModelSerializer):

    class Meta:

        model = Worksheet
        fields = '__all__'


class AllIfoSerializerModelAlt(serializers.Serializer):
    client_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50, source='client.name')
    first_name = serializers.CharField(max_length=50, source='client.first_name')
    last_name = serializers.CharField(max_length=50, source='client.last_name')
    username = serializers.CharField(max_length=50, source='client.username')
    target_link = serializers.URLField(max_length=50)
    category_id = serializers.IntegerField()
    category_name = serializers.CharField(max_length=100, source='category.name')
    price = serializers.IntegerField()
    was_advertised = serializers.BooleanField()
    what_after = serializers.CharField(max_length=200)
