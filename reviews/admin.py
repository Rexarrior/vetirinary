from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'pet_name', 'rating', 'is_published', 'created_at')
    list_filter = ('rating', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('author_name', 'pet_name', 'text')
    readonly_fields = ('created_at',)
