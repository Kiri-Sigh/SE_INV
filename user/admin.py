
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "profile_picture")}),
        (_("Enrollment Details"), {"fields": ("enrolled_year", "enrolled_department", "merit", "level")}),
        (_("Authentication"), {"fields": ("google_id",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2"),
        }),
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:  # Only hash password if changed
            obj.set_password(obj.password)
        obj.save()

admin.site.register(CustomUser, CustomUserAdmin)
