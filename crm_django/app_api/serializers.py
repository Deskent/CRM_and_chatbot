from rest_framework import serializers


class SetOrderSerializerModel(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    first_name = serializers.CharField(allow_null=True,allow_blank=True, max_length=50)
    last_name = serializers.CharField(allow_null=True, max_length=50)
    username = serializers.CharField(allow_null=True, max_length=50)
    category_id = serializers.IntegerField()
    poll = serializers.JSONField()
