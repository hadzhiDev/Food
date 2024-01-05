from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as url_doc

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('food', views.FoodViewSet)
router.register('food-sizes', views.FoodSizeViewSet)
router.register('food-makeup', views.FoodMakeupViewSet)
router.register('food-weight', views.FoodWeightViewSet)
router.register('orders', views.OrderViewSet)
router.register('order-food', views.OrderingFoodViewSet)


urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += url_doc
