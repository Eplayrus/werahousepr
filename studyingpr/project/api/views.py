from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Warehouse, Product, Supply, Order
from .serializers import UserSerializer, WarehouseSerializer, ProductSerializer, SupplySerializer, OrderSerializer

# Регистрация пользователя
class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Аутентификация пользователя (используем стандартный механизм DRF)
# Включить в urls.py маршруты для аутентификации с использованием token или session.

# Создание склада
class WarehouseCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            warehouse = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Создание товара
class ProductCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Поставить товар на склад (только для поставщиков)
class SupplyProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role != 'supplier':
            return Response({"detail": "Только поставщик может поставлять товар"}, status=status.HTTP_403_FORBIDDEN)

        serializer = SupplySerializer(data=request.data)
        if serializer.is_valid():
            supply = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Заказать товар с склада (только для потребителей)
class OrderProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role != 'consumer':
            return Response({"detail": "Только потребитель может забирать товар"}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = serializer.save(consumer=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
