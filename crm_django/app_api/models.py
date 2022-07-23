from django.db import models
from django.core.validators import MinValueValidator
from dataclasses import dataclass


@dataclass
class Worksheet:
    telegram_id: int = None
    name: str = None
    first_name: str = None
    last_name: str = None
    username: str = None
    target_link: str = None
    category: str = None
    price: int = None
    was_advertised: bool = None
    what_after: str = None

    def as_dict(self) -> dict:
        return self.__dict__


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.CharField(max_length=100, verbose_name='Описание категории')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория {self.name}'


class Client(models.Model):
    name = models.CharField(default='', blank=True, max_length=50, verbose_name='Имя клиента')
    first_name = models.CharField(default='', blank=True, max_length=50, verbose_name='Имя')
    last_name = models.CharField(default='', blank=True, max_length=50, verbose_name='Фамилия')
    username = models.CharField(default='', blank=True, max_length=50, verbose_name='Ник')
    telegram_id = models.BigIntegerField(verbose_name='Телеграм ID')
    note = models.TextField(default='', blank=True, max_length=1500, verbose_name='описание')

    class Meta:
        db_table = 'clients'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'Клиент: имя-{self.name}, телеграм ID-{self.telegram_id}'


class Order(models.Model):
    client = models.ForeignKey(Client, related_name='orders', on_delete=models.CASCADE)
    target_link = models.URLField(verbose_name='Целевая ссылка')
    category = models.ForeignKey(
        Category, related_name='client', verbose_name='Категория', on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Цена')
    was_advertised = models.BooleanField(default=False, verbose_name='Была реклама')
    # TODO can be a URL?
    what_after = models.CharField(max_length=100, verbose_name='Что после')

    def __str__(self):
        return f'Заказ №{self.id}'

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
# Order.objects.select_related('client').select_related('category').all()[0].__dict__
