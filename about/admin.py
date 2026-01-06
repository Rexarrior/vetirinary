from django.contrib import admin
from .models import AboutContent, Veterinarian, FeatureItem, AboutPageText

@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order',)

@admin.register(FeatureItem)
class FeatureItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(AboutPageText)
class AboutPageTextAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
