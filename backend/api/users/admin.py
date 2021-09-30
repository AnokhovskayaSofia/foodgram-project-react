from django.contrib import admin
from import_export.admin import ImportMixin
from django.contrib.auth.admin import UserAdmin

from .models import User, SubscribedUser
from .resources import SubscribedUserResource


class SubscribedUserAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = SubscribedUserResource


admin.site.register(User, UserAdmin)
admin.site.register(SubscribedUser, SubscribedUserAdmin)