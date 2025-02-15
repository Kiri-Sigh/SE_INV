from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from your_app.models import StudentUser

class StudentUserAdmin(UserAdmin):  # Use Django’s built-in UserAdmin
    fieldsets = UserAdmin.fieldsets + (  # Add extra fields
        ('Student Info', {'fields': ('enrolled_year', 'enrolled_department', 'merit', 'level')}),
    )

admin.site.register(StudentUser, StudentUserAdmin)
