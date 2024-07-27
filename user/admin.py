# webapp/user/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Notifications, Wallet
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Define the list of fields you want to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name',
                     'user_scope', 'is_active',)

    # Add filters for user attributes
    list_filter = ('is_active', 'is_staff')

    # Customize the fieldsets as needed, making sure to include your custom fields
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'designation',
                        'user_scope', 'mobile_number', 'is_active', 'referred_by',
                       'is_staff', 'is_superuser')
        }),
    )

    # Customize the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'designation',
                       'department_id', 'user_scope', 'mobile_number'),
        }),
    )


# Temple Master
class NotificationResource(resources.ModelResource):
    class Meta:
        model = Notifications


class NotificationAdmin(ImportExportModelAdmin):
    readonly_fields = ('uuid', 'msg_id', 'user', 'created_by')
    resource_class = NotificationResource


# Temple Master
class WalletResource(resources.ModelResource):
    class Meta:
        model = Wallet


class WalletAdmin(ImportExportModelAdmin):
    readonly_fields = ('uuid', 'user', 'from_user', 'txn_type', 'code', 'points', 'created_by')
    resource_class = WalletResource


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Notifications, NotificationAdmin)
admin.site.register(Wallet, WalletAdmin)
