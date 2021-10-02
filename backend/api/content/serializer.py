from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import (Favourite, Ingredient, IngredientsRecipe, Recipe,
                     Shopping, Tag)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'measurement_unit')
        model = Ingredient


class AddIngredientsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
                                        read_only=True,
                                        source='ingredient.measurement_unit')

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount', )
        model = IngredientsRecipe


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = UserSerializer()
    name = serializers.CharField(read_only=True)
    ingredients = AddIngredientsSerializer(source='recipe_content', 
                                           many=True,
                                           read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    image = serializers.ImageField()
    cooking_time = serializers.DecimalField(max_digits=4, decimal_places=1)
    is_favourite = serializers.SerializerMethodField('check_is_favourite')
    is_in_shopping = serializers.SerializerMethodField('check_is_in_shopping')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            ingredients = self.context['request'].data['ingredients']
            ingr_list = []
            for ingr in ingredients:
                ingredient = get_object_or_404(Ingredient, id=ingr['id'])
                if ingredient in ingr_list:
                    raise serializers.ValidationError(
                        f'вы несколько раз используете {ingredient.name}'
                    )
                if float(ingr['amount']) < 0:
                    raise serializers.ValidationError(
                        f'вы ввели отрицательное количество {ingredient.name}'
                    )
            tags = self.context['request'].data['tags']
            tag_list = []
            for tag in tags:
                tag = get_object_or_404(Tag, id=tag['id'])
                if tag in tag_list:
                    raise serializers.ValidationError(
                        f'вы несколько раз используете {tag.name}'
                    )
            if self.context['request'].data['cooking_time'] <= 0:
                raise serializers.ValidationError(
                    f'вы ввели отрицательное или нулевое время приготовления')
            return data

    def ingtedient_create(self, ingredients, recipe):
        for ingredient in ingredients:
            obj = get_object_or_404(Ingredient, id=ingredient['id'])
            amount = ingredient['amount']
            if IngredientsRecipe.objects.filter(recipe=recipe,
                                                ingredient=obj).exists():
                amount += F('amount')
            IngredientsRecipe.objects.update_or_create(recipe=recipe,
                                                       ingredient=obj,
                                                       defaults={'amount': amount})

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.ingtedient_create(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.ingtedient_create(ingredients, instance)
        if 'tags' in self.initial_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def check_is_favourite(self, obj):
        user = self.context.get('request').user.id
        return Favourite.objects.filter(user=user, recipe=obj).exists()

    def check_is_in_shopping(self, obj):
        user = self.context.get('request').user.id
        return Shopping.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favourite',
                  'is_in_shopping',
                  'name',
                  'image',
                  'text',
                  'cooking_time')


class ShortRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    image = serializers.ImageField()
    cooking_time = serializers.DecimalField(max_digits=4,
                                            decimal_places=1)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
