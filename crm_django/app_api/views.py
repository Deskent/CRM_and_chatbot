from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from rest_framework.generics import (
    views, ListAPIView, GenericAPIView, RetrieveAPIView, CreateAPIView)
from app_api.serializers import (
    CategorySerializerModel,
    ClientSerializerModel,
    AllIfoSerializerModel,
    AllIfoSerializerModelAlt,
    TextsSerializerModel, SetOrderSerializerModel,
)
from app_api.models import Client, Category, Order, Texts
from app_api.services import DBITexts, DBIClient, DBIOrder

from django.db.models.manager import Manager


class GetWorksheetsViewSet(ListAPIView, GenericAPIView):
    serializer_class = AllIfoSerializerModelAlt
    queryset = Order.objects.select_related('client').select_related('category').all()

    def get(self, request, *args, **kwargs):
        return self.list(request)


class GetCategoriesViewSet(ListAPIView, GenericAPIView):
    serializer_class = CategorySerializerModel
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request)


class GetTextsViewSet(views.APIView):
    data = DBITexts.get_texts()

    def get(self, request, *args, **kwargs):
        data = self.data
        return JsonResponse(data=data, safe=False)


class SetWorksheetsViewSet(CreateAPIView, GenericAPIView):
    serializer_class = SetOrderSerializerModel
    queryset = Order

    def perform_create(self, serializer):
        data = serializer.data
        client = DBIClient.get_dict(**data)
        client, client_create = Client.objects.get_or_create(**client)
        order = DBIOrder.get_dict(**data)
        order['client_id'] = client.id
        order, order_create = Order.objects.get_or_create(**order)

    def get(self, request, *args, **kwargs):
        return self.create(request)
