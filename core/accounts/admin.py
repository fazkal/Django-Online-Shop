from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "type" ,"is_superuser", "is_active", "is_verified")
    list_filter = ("email", "type" ,"is_superuser", "is_active", "is_verified")
    searching_fields = ("email",)
    ordering = ("email",)
# set fieldset for enable display and edit users
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions","type"),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
# set add_fieldset for enable fill the fields and create user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "type",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )


class CustomProfileAdmin(admin.ModelAdmin):

    list_display = ("user","first_name", "last_name")
    search_fields = ("email",)


admin.site.register(Profile,CustomProfileAdmin)
admin.site.register(User, CustomUserAdmin)