from django.urls import path, include
from app_api.views import (
    GetCategoriesViewSet,
    SetWorksheetsViewSet,
    GetPollByCategoryViewSet
)

urlpatterns = [
    path('send_worksheet', SetWorksheetsViewSet.as_view(), name='send_worksheet'),
    path('get_categories/', GetCategoriesViewSet.as_view(), name='get_categories'),
    path('get_poll_by_category/<int:category_id>', GetPollByCategoryViewSet.as_view(), name='get_poll_by_category'),
]
