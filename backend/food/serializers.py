
from rest_framework import serializers
from .models import Ingredient, Food, FoodRate
from authentication.serializers import UserSerializer

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['pk','name']

class FoodSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many = True, required = False)
    
    class Meta:
        model = Food
        fields = ['pk','name','recipe', 'photo', 'about', 'avg_score', 'create_at', 'author', 'ingredients']
        extra_kwargs = {'author':{'required':False},}
        
    def create(self, validated_data):
        ing_data = validated_data.pop('ingredients', [])
        food_instance = Food.objects.create(**validated_data)
        for ing_name in ing_data:
            ing_obj, created = Ingredient.objects.get_or_create(name = ing_name['name'], food = food_instance)
            food_instance.ingredients.add(ing_obj)
        return food_instance
    
class FoodRateSerializer(serializers.ModelSerializer):
    author = UserSerializer(required = False)

    class Meta:
        model = FoodRate
        fields = "__all__"
        extra_kwargs = {'food':{'required':False},}    
    
    def validate(self, attrs):
        rate = attrs['rate']
        
        if rate > 10:
            raise serializers.ValidationError('Rate must be less than 10')
        if rate < 0:
            raise serializers.ValidationError('Rate must be more than 0')
        
        return attrs
    
    def create(self, validated_data):
        food_rate = FoodRate.objects.create(**validated_data)
        food_rate_list = FoodRate.objects.filter(food = food_rate.food.id).values('rate')
        food = Food.objects.get(pk = food_rate.food.id)
        food.avg_score = sum(food_rate_list)/len(food_rate_list)
        food.save()
        return food_rate
        