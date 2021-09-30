from django.contrib.auth import get_user_model
from rest_framework import serializers


from .models import User, SubscribedUser


User = get_user_model()


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(max_length=200)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
        lookup_field = 'username'

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user.id
        return SubscribedUser.objects.filter(user=user,
                                             user_subscribed_to=obj).exists()


class SubscribeSerializer(UserSerializer):
    # from content.serializer import ShortRecipeSerializer
    # username = serializers.CharField(read_only=True, source='user_subscribed_to.username')
    # email = serializers.EmailField(read_only=True, source='user_subscribed_to.email')
    # first_name = serializers.CharField(read_only=True, source='user_subscribed_to.first_name')
    # last_name = serializers.CharField(read_only=True, source='user_subscribed_to.last_name')

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_recipes(self, obj):
        from content.serializer import ShortRecipeSerializer
        limit = 10
        try:
            limit = self.context['request'].query_params['recipes_limit']
        except Exception:
            pass
        queryset = obj.recipes.all()[:int(limit)]
        serializer = ShortRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_is_subscribed(self, _):
        return True

    def get_recipes_count(self, obj):
        recipes_count = obj.recipes.count()
        return recipes_count
