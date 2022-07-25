from django.http import JsonResponse
from rest_framework.generics import (
    views, ListAPIView, GenericAPIView, CreateAPIView)

from app_api.models import Client, Order
from app_api.serializers import (
    AllIfoSerializerModelAlt,
    SetOrderSerializerModel,
)
from app_api.services import DBITexts, DBIClient, DBIOrder, DBICategories


class GetWorksheetsViewSet(ListAPIView, GenericAPIView):
    serializer_class = AllIfoSerializerModelAlt
    queryset = Order.objects.select_related('client').select_related('category').all()

    def get(self, request, *args, **kwargs):
        return self.list(request)


class GetCategoriesViewSet(views.APIView):
    data = DBICategories.get_texts

    def get(self, request, *args, **kwargs):
        data = self.data()
        return JsonResponse(data=data, safe=False)


class GetTextsViewSet(views.APIView):
    data = DBITexts.get_texts

    def get(self, request, *args, **kwargs):
        data = self.data()
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
