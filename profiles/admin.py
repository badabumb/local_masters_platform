from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'city', 'is_master')
    list_filter = ('is_master', 'city')
    search_fields = ('user__username', 'name', 'city')
