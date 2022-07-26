from django.contrib import admin

from app_api.models import Client, Category, Order, Poll, Answer


# class OrderInline(admin.TabularInline):
#     model = Order


class ClientAdminModel(admin.ModelAdmin):
    list_display = ['username', 'name', 'last_name', 'first_name']
    list_editable = ['name']
    list_filter = ['name']
    search_fields = ['name', 'username']


class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['id', 'name']


class AnswerAdminModel(admin.TabularInline):
    model = Answer
    # list_display = ['id', 'order', 'question', 'answer']
    # readonly_fields = ['order']
    # inlines = [OrderInline]


class PollAdminModel(admin.ModelAdmin):
    list_display = ['category', 'order_number', 'text']
    list_editable = ['order_number', 'text']
    list_filter = ['category']
    search_fields = ['text']


class OrderAdminModel(admin.ModelAdmin):
    list_display = ['id', 'category', 'client']
    list_filter = ['client', 'category']
    search_fields = ['client', 'category']
    list_editable = ['category']
    inlines = [AnswerAdminModel]

admin.site.register(Client, ClientAdminModel)
admin.site.register(Category, CategoryAdminModel)
admin.site.register(Order, OrderAdminModel)
admin.site.register(Poll, PollAdminModel)
# admin.site.register(Answer, AnswerAdminModel)

