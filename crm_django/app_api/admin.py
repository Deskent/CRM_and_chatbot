from django.contrib import admin

from app_api.models import Client, Category, Order, Texts


class ClientAdminModel(admin.ModelAdmin):
    list_display = ['username', 'name', 'last_name', 'first_name']
    list_editable = ['name']
    list_filter = ['name']
    search_fields = ['name', 'username']


class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['id', 'description']
    list_editable = ['description']


class OrderAdminModel(admin.ModelAdmin):
    list_display = ['id', 'category', 'price', 'what_after']
    list_filter = ['client', 'category']
    search_fields = ['client', 'category']
    list_editable = ['category', 'price', 'what_after']


class TextsAdminModel(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'description']
    list_editable = ['title', 'text', 'description']


admin.site.register(Client, ClientAdminModel)
admin.site.register(Category, CategoryAdminModel)
admin.site.register(Order, OrderAdminModel)
admin.site.register(Texts, TextsAdminModel)

