from django.contrib import admin
from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_rss', 'is_active', 'created_at']
    list_filter = ['is_rss', 'is_active']
    search_fields = ['name', 'url']