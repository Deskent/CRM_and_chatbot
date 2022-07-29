from typing import Callable

from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework.generics import (
    views, GenericAPIView, CreateAPIView)

from app_api.models import Client, Order, Answer
from app_api.serializers import (
    SetOrderSerializerModel,
)
from app_api.services import DBIClient, DBIOrder, DBICategories, DBIPoll


class GetCategoriesViewSet(views.APIView):
    get_data = DBICategories.get_categories

    def get(self, request, *args, **kwargs):
        data = self.get_data()
        return JsonResponse(data=data, safe=False)


class GetPollByCategoryViewSet(views.APIView):
    get_data: Callable = DBIPoll.get_poll

    def get(self, request, *args, **kwargs):
        data: list[str] = self.get_data(category_id=kwargs['category_id'])
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

        answers = [
            Answer(**{'order_id': order.id, 'question': question, 'answer': answer})
            for question, answer in data.get('poll')
        ]

        Answer.objects.bulk_create(answers)

    def get(self, request, *args, **kwargs):
        return self.create(request)


class GrabberView(TemplateView):
    template_name = 'app_api/grabber.html'
    extra_context = {'title': 'Grabber'}


class MainView(TemplateView):
    template_name = 'app_api/main.html'
    extra_context = {'title': 'Главная'}
