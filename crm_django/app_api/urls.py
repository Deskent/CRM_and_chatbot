from django.urls import path, include
from app_api.views import (
    GetWorksheetsViewSet, GetTextsViewSet, GetCategoriesViewSet, SetWorksheetsViewSet)

urlpatterns = [
    path('get_worksheet', GetWorksheetsViewSet.as_view(), name='get_worksheet'),
    path('send_worksheet', SetWorksheetsViewSet.as_view(), name='send_worksheet'),
    path('get_categories', GetCategoriesViewSet.as_view(), name='get_categories'),
    path('get_texts', GetTextsViewSet.as_view(), name='get_texts'),
]
