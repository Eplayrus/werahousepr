from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Кастомная модель пользователя.

    Атрибуты:
        ROLE_CHOICES (tuple): Варианты ролей пользователя (поставщик, потребитель).
        role (str): Роль пользователя в системе.
    """
    ROLE_CHOICES = [
        ('supplier', 'Поставщик'),
        ('consumer', 'Потребитель'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class Warehouse(models.Model):
    """
    Модель склада.

    Атрибуты:
        name (str): Название склада.
        location (str): Местоположение склада.
    """
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)


class Product(models.Model):
    """
    Модель товара.

    Атрибуты:
        name (str): Название товара.
        quantity (int): Количество товара на складе.
        price (float): Цена товара.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Supply(models.Model):
    """
    Модель поставки товара.

    Атрибуты:
        warehouse (Warehouse): Склад, на который поставляется товар.
        product (Product): Товар, который поставляется.
        quantity (int): Количество поставляемого товара.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    """
    Модель заказа товаров с склада.

    Атрибуты:
        product (Product): Товар, который заказывает потребитель.
        warehouse (Warehouse): Склад, с которого будет списываться товар.
        quantity (int): Количество заказываемого товара.
        consumer (User): Потребитель, который оформляет заказ.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    consumer = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Сохранение заказа с проверкой наличия достаточного количества товара на складе.

        Исключения:
            ValueError: Если товара на складе недостаточно для выполнения заказа.
        """
        available_quantity = Supply.objects.filter(warehouse=self.warehouse, product=self.product).first().quantity
        if available_quantity < self.quantity:
            raise ValueError("Недостаточно товара на складе")
        super().save(*args, **kwargs)
