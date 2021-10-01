from import_export import resources

from .models import SubscribedUser, User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name',)


class SubscribedUserResource(resources.ModelResource):
    class Meta:
        model = SubscribedUser
        fields = ('id', 'user', 'user_subscribed_to',)
