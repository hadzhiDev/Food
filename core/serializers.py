from rest_framework import serializers
# from drf_writable_nested.serializers import WritableNestedModelSerializer

from core.models import Category, Food, Size, FoodMakeup, FoodWeight, OrderingFood, Order


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class FoodMakeupForFoodCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodMakeup
        exclude = ('food', )


class SizeForFoodCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        exclude = ('food', )


class FoodWeightForFoodCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodWeight
        exclude = ('food', )


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'


class CreateFoodSerializer(serializers.ModelSerializer):
    makeups = FoodMakeupForFoodCreationSerializer(many=True)
    sizes = SizeForFoodCreationSerializer(many=True)
    weight = FoodWeightForFoodCreationSerializer(many=True)

    def create(self, validated_data):
        makeups = validated_data.pop('makeups', [])
        sizes = validated_data.pop('sizes', [])
        weight = validated_data.pop('weight', [])
        food = super().create(validated_data)
        makeups_serializer = FoodMakeupForFoodCreationSerializer(data=makeups)
        makeups_serializer.is_valid(raise_exception=True)
        makeups_serializer.save(food=food)
        sizes_serializer = SizeForFoodCreationSerializer(data=sizes)
        sizes_serializer.is_valid(raise_exception=True)
        sizes_serializer.save(food=food)
        weight_serializer = FoodWeightForFoodCreationSerializer(data=weight)
        weight_serializer.is_valid(raise_exception=True)
        weight_serializer.save(food=food)

        return food

    class Meta:
        model = Food
        fields = '__all__'


class ReadFoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    makeups = FoodMakeupForFoodCreationSerializer(many=True)
    sizes = SizeForFoodCreationSerializer(many=True)
    weight = FoodWeightForFoodCreationSerializer(many=True)

    class Meta:
        model = Food
        fields = '__all__'


class FoodSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class FoodMakeupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodMakeup
        fields = '__all__'


class FoodWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodWeight
        fields = '__all__'


class OrderingFoodForReadOrderSerializer(serializers.ModelSerializer):
    food = ReadFoodSerializer(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = OrderingFood
        fields = ('food', 'quantity', 'total_price', 'size',)


class OrderSerializer(serializers.ModelSerializer):
    ordering_food = OrderingFoodForReadOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        total_price = sum(item.total_price for item in instance.ordering_food.all())
        ret.setdefault('total_price', total_price)
        return ret


class OrderingFoodForCreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderingFood
        fields = ('food', 'quantity', 'size')


class CreateOrderSerializer(serializers.ModelSerializer):
    ordering_food = OrderingFoodForCreateOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        if len(attrs['name']) < 3:
            raise serializers.ValidationError({
                'name': [
                    'Name must be at least 3 characters'
                ]
            })

        return attrs

    # def validate_home(self, value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError(['Home must be at least 3 characters'])
    #     return value

    def create(self, validated_data):
        food = validated_data.pop('ordering_food', [])
        order = Order.objects.create(**validated_data)
        for item in food:
            OrderingFood.objects.create(**item, order=order)
        return order


class OrderingFoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderingFood
        fields = '__all__'
