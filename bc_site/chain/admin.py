from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import BlockStruct, TxModel, AccountModel
# Register your models here

admin.site.register(BlockStruct)
admin.site.register(TxModel)
#admin.site.register(AccountModel)

class AccountModelInline(admin.StackedInline):
    model = AccountModel
    can_delete = False
    verbose_name_plural = "accounts"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [AccountModelInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
