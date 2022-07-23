from django.contrib import admin

from app_api.models import Client, Category, Order


class ClientAdminModel(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name', 'id', 'telegram_id']


class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['id', 'name']


class OrderAdminModel(admin.ModelAdmin):
    list_display = ['id', 'category', 'price', 'what_after']
    list_filter = ['client', 'category']
    search_fields = ['client']
    list_editable = ['category', 'price', 'what_after']


admin.site.register(Client, ClientAdminModel)
admin.site.register(Category, CategoryAdminModel)
admin.site.register(Order, OrderAdminModel)

