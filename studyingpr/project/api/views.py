from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Warehouse, Product, Supply, Order
from .serializers import UserSerializer, WarehouseSerializer, ProductSerializer, SupplySerializer, OrderSerializer

class RegisterUserView(APIView):
    """
    API для регистрации нового пользователя.

    Метод:
        post: Создает нового пользователя на основе переданных данных.

    Ответы:
        201 Created: Успешная регистрация.
        400 Bad Request: Ошибка валидации данных.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WarehouseCreateView(APIView):
    """
    API для создания склада.

    Доступ:
        Только аутентифицированные пользователи.

    Метод:
        post: Создает новый склад.

    Ответы:
        201 Created: Склад успешно создан.
        400 Bad Request: Ошибка валидации данных.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            warehouse = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductCreateView(APIView):
    """
    API для создания товара.

    Доступ:
        Только аутентифицированные пользователи.

    Метод:
        post: Создает новый товар.

    Ответы:
        201 Created: Товар успешно создан.
        400 Bad Request: Ошибка валидации данных.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer
