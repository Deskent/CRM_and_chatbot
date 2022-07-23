from django.urls import path, include
from app_api.views import GetWorksheetsViewSet

urlpatterns = [
    path('get_worksheet/', GetWorksheetsViewSet.as_view(), name='get_worksheet'),
    path('send_worksheet/', GetWorksheetsViewSet.as_view(), name='send_worksheet'),
    path('get_categories/', GetWorksheetsViewSet.as_view(), name='get_categories'),
    path('get_texts/', GetWorksheetsViewSet.as_view(), name='get_texts'),
]
