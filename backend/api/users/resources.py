from import_export import resources

from .models import SubscribedUser


class SubscribedUserResource(resources.ModelResource):
    class Meta:
        model = SubscribedUser
        fields = ('id', 'user', 'recipe',)