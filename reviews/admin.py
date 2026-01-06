from django.contrib import admin
from .models import Review, ReviewsPageText


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'pet_name', 'rating', 'is_published', 'created_at')
    list_filter = ('rating', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('author_name', 'pet_name', 'text')
    readonly_fields = ('created_at',)


@admin.register(ReviewsPageText)
class ReviewsPageTextAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
