from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import User, Team, Membership, Profile
from .forms import CustomAuthenticationForm, CustomContentTypeAdminForm

admin.site.login_form = CustomAuthenticationForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["email", "is_staff"]
    ordering = ["email"]
    readonly_fields = ('password',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2"
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {
         "fields": ("last_login", "date_joined")}),
    )


@admin.register(Team)
class TeamModelAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


@admin.register(Membership)
class MemeberModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)
    fieldsets = (
        (None, {"fields": ("holder", "team", "permissions", "deleted")}),
    )


admin.site.register(Permission)
admin.site.register(Profile)


@admin.register(ContentType)
class ContentTypeModelAdmin(admin.ModelAdmin):
    form = CustomContentTypeAdminForm
