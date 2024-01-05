from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from core.filters import FoodFilter
from core.models import Category, Food, Size, FoodMakeup, FoodWeight, OrderingFood, Order
from core.paginations import SimpleResultPagination
from core.serializers import (CategorySerializer, FoodSerializer, CreateFoodSerializer, ReadFoodSerializer,
                              FoodMakeupSerializer, FoodSizeSerializer, FoodWeightSerializer,
                              OrderSerializer, OrderingFoodSerializer, CreateOrderSerializer)
from core.mixins import SerializeByActionMixin, UltraModelViewSet


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = CategorySerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    permission_classes = (IsAuthenticated, )


class FoodViewSet(SerializeByActionMixin, ModelViewSet):
    queryset = Food.objects.all()
    pagination_class = SimpleResultPagination
    serializer_classes = {
        'list': ReadFoodSerializer,
        'update': FoodSerializer,
        'create': CreateFoodSerializer,
        'retrieve': ReadFoodSerializer,
    }
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name',]
    ordering_fields = ['name',]
    filterset_class = FoodFilter
    permission_classes = (IsAuthenticated,)


class FoodSizeViewSet(ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = FoodSizeSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'price']
    filterset_fields = ['food']
    permission_classes = (IsAuthenticated,)


class FoodMakeupViewSet(ModelViewSet):
    queryset = FoodMakeup.objects.all()
    serializer_class = FoodMakeupSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name',]
    filterset_fields = ['food',]
    permission_classes = (IsAuthenticated,)


class FoodWeightViewSet(ModelViewSet):
    queryset = FoodWeight.objects.all()
    serializer_class = FoodWeightSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['value',]
    filterset_fields = ['food',]
    permission_classes = (IsAuthenticated,)


class OrderViewSet(UltraModelViewSet):
    queryset = Order.objects.all()
    serializer_classes = {
        'list': OrderSerializer,
        'retrieve': OrderSerializer,
        'update': OrderSerializer,
        'create': CreateOrderSerializer,
    }
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    search_fields = ['name', 'email', 'phone', 'address', 'home']
    filterset_fields = ['ordering_food__food']
    permission_classes = (AllowAny,)


class OrderingFoodViewSet(UltraModelViewSet):
    queryset = OrderingFood.objects.all()
    serializer_class = OrderingFoodSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'quantity']
    filterset_fields = ['food', 'order']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (AllowAny,),
        'update': (IsAuthenticated, IsAdminUser,),
        'destroy': (IsAuthenticated, IsAdminUser,),
    }


