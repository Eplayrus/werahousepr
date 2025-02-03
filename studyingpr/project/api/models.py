from django.db import models
from django.contrib.auth.models import AbstractUser

# Пользователь с ролью
class User(AbstractUser):
    ROLE_CHOICES = [
        ('supplier', 'Поставщик'),
        ('consumer', 'Потребитель'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Изменение related_name для конфликтующих полей
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

# Склады
class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

# Товары
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Поставки товаров на склад
class Supply(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

# Заказы товаров с склада
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    consumer = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Проверка наличия товара на складе
        available_quantity = Supply.objects.filter(warehouse=self.warehouse, product=self.product).first().quantity
        if available_quantity < self.quantity:
            raise ValueError("Недостаточно товара на складе")
        super().save(*args, **kwargs)
