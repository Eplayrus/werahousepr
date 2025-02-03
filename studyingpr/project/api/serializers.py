from rest_framework import serializers
from .models import User, Warehouse, Product, Supply, Order

# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Сериализатор для склада
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location']

# Сериализатор для товара
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']

# Сериализатор для поставки товара
class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = ['id', 'product', 'warehouse', 'quantity']

# Сериализатор для заказа товара
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'warehouse', 'quantity', 'consumer']
