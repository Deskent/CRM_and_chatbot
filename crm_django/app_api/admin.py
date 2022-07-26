from django.contrib import admin

from app_api.models import Client, Category, Order, Texts, Poll, Answer


class ClientAdminModel(admin.ModelAdmin):
    list_display = ['username', 'name', 'last_name', 'first_name']
    list_editable = ['name']
    list_filter = ['name']
    search_fields = ['name', 'username']


class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['id', 'description']
    list_editable = ['description']


class AnswerAdminModel(admin.ModelAdmin):
    list_display = ['id', 'order', 'question', 'answer']
    readonly_fields = ['order']


class PollAdminModel(admin.ModelAdmin):
    list_display = ['category', 'order_number', 'text']
    list_editable = ['order_number', 'text']
    list_filter = ['category']
    search_fields = ['text']


class OrderAdminModel(admin.ModelAdmin):
    list_display = ['id', 'category']
    list_filter = ['client', 'category']
    search_fields = ['client', 'category']
    list_editable = ['category']


class TextsAdminModel(admin.ModelAdmin):
    list_display = ['id', 'text', 'description']
    list_editable = ['text', 'description']
    readonly_fields = ['title']


admin.site.register(Client, ClientAdminModel)
admin.site.register(Category, CategoryAdminModel)
admin.site.register(Order, OrderAdminModel)
admin.site.register(Texts, TextsAdminModel)
admin.site.register(Poll, PollAdminModel)
admin.site.register(Answer, AnswerAdminModel)

