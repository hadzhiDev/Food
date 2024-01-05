from django.db import models
from django.core.exceptions import ValidationError

from django_resized import ResizedImageField

from phonenumber_field.modelfields import PhoneNumberField

from utils.models import TimeStampAbstractModel


class Category(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField('название', max_length=200, unique=True)

    def __str__(self):
        return f'{self.name}'


class Food(TimeStampAbstractModel):

    name = models.CharField('название', max_length=100)
    image = ResizedImageField('изображение', upload_to='food_images/', force_format='WEBP', quality=90)
    description = models.CharField('описание', max_length=255, help_text='Просто описание')
    category = models.ForeignKey('core.Category', models.PROTECT, verbose_name='категория',
                                 help_text='Выберите категорию')

    class Meta:
        verbose_name = 'блюда'
        verbose_name_plural = 'блюда'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.name}'


class Size(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'размер'
        verbose_name_plural = 'размеры'

    name = models.CharField('название', max_length=150, unique=True)
    price = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0.0)
    food = models.ForeignKey('core.Food', models.CASCADE, 'sizes', verbose_name='блюда')

    def __str__(self):
        return f'{self.name} - {self.price}'


class FoodMakeup(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'состав блюда'
        verbose_name_plural = 'состав блюда'
        ordering = ('-created_at',)

    name = models.CharField('название', max_length=100)
    food = models.ForeignKey('core.Food', models.CASCADE, 'makeups', verbose_name='блюда')

    def __str__(self):
        return f'{self.name}'


class FoodWeight(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'вес блюда'
        verbose_name_plural = 'весы блюда'
        ordering = ('-created_at',)

    value = models.DecimalField('вес', max_digits=10, decimal_places=3, default=0.0)
    food = models.ForeignKey('core.Food', models.CASCADE, 'weight', verbose_name='блюда')

    def __str__(self):
        return f'{self.value}'


class Order(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created_at',)

    WAITING = 'waiting'
    CANCELED = 'canceled'
    ON_DELIVERY = 'on_delivery'
    DELIVERED = 'delivered'

    ORDER_STATUS = (
        (WAITING, 'В ожидание'),
        (CANCELED, 'Отменено'),
        (ON_DELIVERY, 'Доставляется'),
        (DELIVERED, 'Доставлено')
    )
    name = models.CharField('имя и фамилия', max_length=140)
    email = models.EmailField('электронная почта')
    phone = PhoneNumberField('номер телефона')
    address = models.CharField('адрес', max_length=255)
    home = models.CharField('номер квартара или дома', max_length=150)
    status = models.CharField('статус', choices=ORDER_STATUS, default=WAITING, max_length=20)

    def __str__(self):
        return f'{self.name} - {self.email}'

    @property
    def total_price(self):
        return sum(item.total_price for item in self.ordering_food.all())

    total_price.fget.short_description = 'Итоговая цена'


class OrderingFood(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'блюда для заказа'
        ordering = ('-created_at',)

    # price = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0.0)
    size = models.ForeignKey('core.Size', models.PROTECT,)
    quantity = models.PositiveIntegerField('количество', default=1)
    order = models.ForeignKey('core.Order', models.CASCADE, 'ordering_food', verbose_name='заказ')
    food = models.ForeignKey('core.Food', models.PROTECT, verbose_name='блюда')

    def clean(self):
        if not Size.objects.get(food=self.food, id=self.size.id):
            raise ValidationError({'name': ["the food does not include this size"]})

    @property
    def total_price(self):
        size = Size.objects.get(food=self.food, id=self.size.id)
        if size:
            return size.price * self.quantity

    def __str__(self):
        return f'{self.order} - {self.food}'