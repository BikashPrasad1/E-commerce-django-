from django.contrib import admin
from .models import User


#  Simple User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')