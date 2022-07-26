from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from app_api.models import Client, Category, Order, Poll, Answer


class ClientAdminModel(admin.ModelAdmin):
    list_display = ['username', 'name', 'last_name', 'first_name']
    list_editable = ['name']
    list_filter = ['name']
    search_fields = ['name', 'username']


class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['id', 'name']


class AnswerInlineModel(admin.TabularInline):
    model = Answer
    my_widget = Textarea(attrs={
        "cols": "40", "rows": "3", "class": "vLargeTextField", "maxlength": "1500", "required": ""})
    formfield_overrides = {
        models.TextField: {'widget': my_widget},
    }


class AnswerAdminModel(admin.ModelAdmin):
    model = Answer
    list_display = ['order', 'category', 'client',  'question', 'answer']
    readonly_fields = ['order']

    def category(self, obj):
        return obj.order.category

    category.short_description = 'Категория'

    def client(self, obj):
        return obj.order.client

    client.short_description = 'Клиент'

    my_widget = Textarea(attrs={
        "cols": "40", "rows": "3", "class": "vLargeTextField", "maxlength": "1500", "required": ""})
    formfield_overrides = {
        models.TextField: {'widget': my_widget},
    }


class PollAdminModel(admin.ModelAdmin):
    list_display = ['category', 'order_number', 'text']
    list_editable = ['order_number', 'text']
    list_filter = ['category']
    search_fields = ['text']

    my_widget = Textarea(attrs={
        "cols": "40", "rows": "3", "class": "vLargeTextField", "maxlength": "1500", "required": ""})
    formfield_overrides = {
        models.TextField: {'widget': my_widget},
    }


class OrderAdminModel(admin.ModelAdmin):
    list_display = ['id', 'category', 'client']
    list_filter = ['client', 'category']
    search_fields = ['client', 'category']
    list_editable = ['category']
    inlines = [AnswerInlineModel]


admin.site.register(Client, ClientAdminModel)
admin.site.register(Category, CategoryAdminModel)
admin.site.register(Order, OrderAdminModel)
admin.site.register(Poll, PollAdminModel)
admin.site.register(Answer, AnswerAdminModel)

