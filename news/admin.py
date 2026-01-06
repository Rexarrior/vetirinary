from django.contrib import admin
from .models import News, NewsPageText

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(NewsPageText)
class NewsPageTextAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
