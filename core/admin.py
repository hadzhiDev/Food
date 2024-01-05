from django.contrib import admin
from django import forms

from .models import Category, Food, FoodMakeup, Size, FoodWeight, OrderingFood, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class FoodMakeupStackedInline(admin.TabularInline):

    model = FoodMakeup
    extra = 1


class FoodWeightStackedInline(admin.TabularInline):

    model = FoodWeight
    extra = 1


class SizeStackedInline(admin.TabularInline):

    model = Size
    extra = 1


class FoodAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, label='Описание', help_text='Просто описание')

    class Meta:
        model = Food
        fields = '__all__'


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category',)
    list_display_links = ('id', 'name',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)
    readonly_fields = ('created_at', 'updated_at',)
    form = FoodAdminForm
    inlines = [FoodMakeupStackedInline, SizeStackedInline, FoodWeightStackedInline]


class OrderingFoodStackedInline(admin.StackedInline):
    model = OrderingFood
    extra = 1
    readonly_fields = ('created_at', 'updated_at',)


class OrderAdminForm(forms.ModelForm):

    address = forms.CharField(widget=forms.Textarea, label='Адрес')

    class Meta:
        model = Order
        fields = '__all__'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'total_price', 'status',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name', 'email', 'phone', 'address', 'home',)
    list_filter = ('created_at',)
    readonly_fields = ('total_price', 'created_at', 'updated_at',)
    inlines = (OrderingFoodStackedInline,)
    form = OrderAdminForm
