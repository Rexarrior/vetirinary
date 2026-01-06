from django.contrib import admin
from .models import SiteSettings, CommonPhrase, HeroSection, StatItem

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(CommonPhrase)
class CommonPhraseAdmin(admin.ModelAdmin):
    list_display = ('key', 'text', 'description')
    search_fields = ('key', 'text')

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(StatItem)
class StatItemAdmin(admin.ModelAdmin):
    list_display = ('number', 'label', 'order')
    list_editable = ('order',)
