from django.urls import path, include
from app_api.views import GetWorksheetsViewSet

urlpatterns = [
    path('crm/', GetWorksheetsViewSet.as_view(), name='get_orders')
]
