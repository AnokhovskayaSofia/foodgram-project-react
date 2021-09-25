from .models import Recipe
from rest_framework import serializers
from .models import Tag, Recipe, Ingredient, IngredientsRecipe, Shopping, Favourite
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count, F

class IngredientsSerializer(serializers.ModelSerializer):
    exclude = ('id',)
    model = Ingredient    

class AddIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'ingredient', 'recipe')
        model = IngredientsRecipe    


class TagsSerializer(serializers.ModelSerializer):
    print('serializerTag')
    class Meta:
        fields = ('id', 'name', 'HEX_code', 'slug')
        model = Tag

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True
                                          )
    name = serializers.CharField(read_only=True)
    ingredients = AddIngredientsSerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    image = serializers.ImageField()
    cooking_time = serializers.DecimalField(max_digits=4, decimal_places=1)
    is_favourite = serializers.SerializerMethodField('check_is_favourite')
    is_in_shopping = serializers.SerializerMethodField('check_is_in_shopping')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            obj = get_object_or_404(Ingredient, id=ingredient['id'])
            amount = ingredient['amount']
            if IngredientsRecipe.objects.filter(
                 recipe=recipe,
                 ingredient=obj
                ).exists():
                amount += F('amount')
            IngredientsRecipe.objects.update_or_create(
             recipe=recipe,
             ingredient=obj,
             defaults={'amount': amount}
            )
        return recipe
 
    def update(self, instance, validated_data):
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            for ingredient in ingredients:
                obj = get_object_or_404(Ingredient, id=ingredient['id'])
                amount = ingredient['amount']
                if IngredientsRecipe.objects.filter(
                     recipe=instance,
                     ingredient=obj
                    ).exists():
                    amount += F('amount')
                IngredientsRecipe.objects.update_or_create(
                 recipe=instance,
                 ingredient=obj,
                 defaults={'amount': amount}
                 )
        if 'tags' in self.initial_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)
 
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
             'cooking_time',
             instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    
    def check_is_favourite(self,obj):
        user = self.context.get('request').user
        return Favourite.objects.filter(user=user, recipe=obj).exists()

    def check_is_in_shopping(self, obj):
        user = self.context.get('request').user
        return Shopping.objects.filter(user=user, recipe=obj).exists()
    
    class Meta:
        model = Recipe
        fields = ('__all__')