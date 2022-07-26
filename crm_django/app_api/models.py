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
        ordering = ['id']

    def __str__(self):
        return f'Категория {self.name}'


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя клиента')
    first_name = models.CharField(default='', blank=True, max_length=50, verbose_name='Имя')
    last_name = models.CharField(default='', blank=True, max_length=50, verbose_name='Фамилия')
    username = models.CharField(default='', blank=True, max_length=50, verbose_name='Ник')
    telegram_id = models.BigIntegerField(verbose_name='Телеграм ID')
    description = models.TextField(
        default='', blank=True, max_length=1500, verbose_name='Доп информация')

    class Meta:
        db_table = 'clients'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'Клиент: имя-{self.name}, телеграм ID-{self.telegram_id}'


class Order(models.Model):
    client = models.ForeignKey(Client, related_name='orders', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name='client', verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return f'Заказ №{self.id}'

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Texts(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Поле бота')
    text = models.TextField(max_length=1000, verbose_name='Текст вопроса')
    description = models.CharField(max_length=50, verbose_name='Описание (где будет задан)')

    class Meta:
        db_table = 'texts'
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'


class Poll(models.Model):
    category = models.ForeignKey(
        Category, related_name='poll', verbose_name='Категория', on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, verbose_name='Текст вопроса')
    order_number = models.IntegerField(
        unique=True, validators=[MinValueValidator(1)], verbose_name='Порядковый номер')

    class Meta:
        db_table = 'polls'
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['order_number']


class Answer(models.Model):
    order = models.ForeignKey(
        Order, related_name='answers', verbose_name='Заказ', on_delete=models.CASCADE)
    question = models.TextField(max_length=1500, verbose_name='Вопрос')
    answer = models.TextField(max_length=1500, verbose_name='Ответ')

    class Meta:
        db_table = 'answers'
        ordering = ['order']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
