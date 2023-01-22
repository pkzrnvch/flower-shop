from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from django.core.validators import MinValueValidator
from django.db import models


class ConsultationRequest(models.Model):

    class Status(models.IntegerChoices):
        PROCESSING = 1, 'Обрабатывается'
        PROCESSED = 2, 'Обработана'

    name = models.CharField('имя', max_length=100)
    phone_number = PhoneNumberField(verbose_name='номер телефона')
    acceptance_of_rules = models.BooleanField('согласия с правилами', default=False)
    created = models.DateTimeField('дата', auto_now_add=True)
    status = models.SmallIntegerField(
        'статус',
        choices=Status.choices,
        default=Status.PROCESSING,
    )

    class Meta:
        ordering = ['created', 'status']
        indexes = [
            models.Index(fields=['created', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['phone_number']),
        ]
        verbose_name = 'консультация'
        verbose_name_plural = 'консультации'

    def __str__(self):
        return f'Запись №{self.id}'


class EventTag(models.Model):
    name = models.CharField('название', max_length=100)

    class Meta:
        verbose_name = 'тег события'
        verbose_name_plural = 'теги событий'

    def __str__(self):
        return self.name


class FlowerBouquetAttribute(models.Model):
    name = models.CharField('название', db_index=True, max_length=200)

    class Meta:
        verbose_name = 'атрибут букета'
        verbose_name_plural = 'атрибуты букета'

    def __str__(self):
        return self.name


class Flower(models.Model):

    name = models.CharField('название', max_length=100)
    availability = models.BooleanField('наличие', default=False)
    quantity = models.SmallIntegerField('количество', default=0, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['name']
        verbose_name = 'цветок'
        verbose_name_plural = 'цветы'
        indexes = [
            models.Index(fields=['availability']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class FlowerBouquet(models.Model):

    flowers = models.ManyToManyField(
        Flower,
        verbose_name='цветы',
        related_name='flower_bouquets',
        through='FlowerBouquetItem',
    )
    attributes = models.ManyToManyField(
        FlowerBouquetAttribute,
        verbose_name='атрибуты букета',
        related_name='flower_bouquets',
        through='FlowerBouquetAttributeItem'
    )
    name = models.CharField('букет', max_length=100)
    description = models.TextField('описание', blank=True)
    price = models.DecimalField(
        'цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField('картинка', blank=True, upload_to='flower_bouquets')
    availability = models.BooleanField('наличие', default=False)
    created = models.DateTimeField('создан', auto_now_add=True)
    updated = models.DateTimeField('обновлен', auto_now=True)
    event_tags = models.ManyToManyField(EventTag, related_name='flower_bouquets')
    width = models.SmallIntegerField('ширина', validators=[MinValueValidator(10)], default=10)
    height = models.SmallIntegerField('высота', validators=[MinValueValidator(20)], default=20)

    class Meta:
        ordering = ['name']
        verbose_name = 'букет'
        verbose_name_plural = 'букеты'
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['name']),
            models.Index(fields=['availability']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('flower_shop_app:bouquet_detail', args=[self.id])


class FlowerBouquetAttributeItem(models.Model):
    flower_bouquet = models.ForeignKey(
        FlowerBouquet,
        verbose_name='букет',
        related_name='flower_bouquet_attributes',
        on_delete=models.CASCADE,
    )
    flower_bouquet_attribute = models.ForeignKey(
        FlowerBouquetAttribute,
        verbose_name='атрибут букета',
        related_name='flower_bouquet_attributes',
        on_delete=models.CASCADE,
    )
    attribute_quantity = models.SmallIntegerField(
        'количество атрибутов в букете',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'элемент букета'
        verbose_name_plural = 'элементы букета'

    def __str__(self):
        return 'элемент букета'


class FlowerBouquetItem(models.Model):

    flower = models.ForeignKey(
        Flower,
        verbose_name='цветок',
        related_name='flower_bouquet_items',
        on_delete=models.CASCADE,
    )
    flower_bouquet = models.ForeignKey(
        FlowerBouquet,
        verbose_name='букет',
        related_name='flower_bouquet_items',
        on_delete=models.CASCADE,
    )
    flower_quantity = models.SmallIntegerField(
        'количество цветов в букете',
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'элемент букета'
        verbose_name_plural = 'элементы букета'

    def __str__(self):
        return 'элемент букета'


class OrderQuerySet(models.QuerySet):
    def with_total_price(self):
        return self.annotate(
            total_price=models.Sum(
                models.F('items__flower_bouquet_price') * models.F('items__quantity')
            )
        )


class Order(models.Model):

    class Status(models.IntegerChoices):
        PROCESSING = 1, 'Обрабатывается'
        PREPARING = 2, 'Собирается'
        DELIVER = 3, 'В доставке'
        COMPLETE = 4, 'Выполнен'

    class DeliveryTime(models.IntegerChoices):
        MORNING = 10, 'C 10:00 до 12:00'
        NOON_1 = 12, 'C 12:00 до 14:00'
        NOON_2 = 14, 'C 14:00 до 16:00'
        AFTERNOON = 16, 'C 16:00 до 18:00'
        EVENING = 18, 'C 18:00 до 20:00'

    client_name = models.CharField('имя клиента', max_length=100)
    phone_number = PhoneNumberField('номер телефона')
    address = models.CharField('адрес', max_length=250)
    email = models.EmailField(blank=True)
    created = models.DateTimeField('дата и время заказа', auto_now_add=True)
    delivery_time = models.SmallIntegerField(
        'время доставки',
        choices=DeliveryTime.choices,
        blank=False,
        default=None
    )
    status = models.SmallIntegerField(
        'статус заказа',
        choices=Status.choices,
        default=Status.PROCESSING,
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        ordering = ['status', '-created']
        indexes = [
            models.Index(fields=['status', '-created']),
            models.Index(fields=['phone_number']),
        ]
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ №{self.id}'


class OrderItem(models.Model):

    flower_bouquet = models.ForeignKey(
        FlowerBouquet,
        verbose_name='букет',
        related_name='order_items',
        on_delete=models.PROTECT,
    )
    order = models.ForeignKey(
        Order,
        verbose_name='заказ',
        related_name='items',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField('количество', default=1, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return self.flower_bouquet.name
