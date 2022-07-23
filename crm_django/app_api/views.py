from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import views, ListAPIView, GenericAPIView
from app_api.serializers import (
    CategorySerializerModel, ClientSerializerModel, AllIfoSerializerModel, AllIfoSerializerModelAlt)
from app_api.models import Client, Category, Order


class GetWorksheetsViewSet(ListAPIView, GenericAPIView):
    serializer_class = AllIfoSerializerModelAlt
    queryset = Order.objects.select_related('client').select_related('category').all()

    # def get_queryset(self):
    #     a = self.queryset[0]
    #     print(a.client_name)
    #     aaa = 10

    def get(self, request, *args, **kwargs):
        return self.list(request)

#
# class AddChannelViewSet(CreateAPIView, GenericAPIView):
#     serializer_class = GetChannelsSerializerModel
#
#     def perform_create(self, serializer):
#         DBIChannel.add_channel(**serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request)
