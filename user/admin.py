from django.contrib import admin
from .models import User
from django.contrib.auth.models import UserAdmin


class UserAdmin(admin.ModelAdmin): # Налаштування для моделі User
   pass
    # list_display = ('username', 'email', 'is_staff')


admin.site.register(User, UserAdmin)
