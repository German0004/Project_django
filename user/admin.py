from django.contrib import admin
from models import User
from django.contrib.auth.models import UserAdmin


admin.site.register(User, UserAdmin)

