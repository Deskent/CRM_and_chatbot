from rest_framework import serializers
from app_api.models import (Category, Client, Order, Worksheet, Texts)


class CategorySerializerModel(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TextsSerializerModel(serializers.ModelSerializer):

    class Meta:
        model = Texts
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
    telegram_id = serializers.IntegerField(source='client.telegram_id')
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


class SetOrderSerializerModel(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    target_link = serializers.CharField(max_length=50)
    category = serializers.IntegerField()
    price = serializers.IntegerField()
    was_advertised = serializers.BooleanField()
    what_after = serializers.CharField(max_length=200)

#
# @dataclass
# class Worksheet:
#
#     name: str = None
#     first_name: str = None
#     last_name: str = None
#     username: str = None
#     target_link: str = None
#     category: str = None
#     price: int = None
#     was_advertised: bool = None
#     what_after: str = None
#
#     def as_dict(self) -> dict:
#         return self.__dict__
