from django.contrib import admin
from .models import ContactInfo, ContactSubmission

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('clinic_name', 'phone', 'email', 'has_coordinates')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('clinic_name', 'address', 'phone', 'email', 'working_hours')
        }),
        ('Яндекс Карты - координаты', {
            'fields': ('latitude', 'longitude', 'map_zoom'),
            'description': 'Укажите координаты для отображения карты. Координаты можно найти на Яндекс.Картах, кликнув правой кнопкой по нужной точке.'
        }),
        ('Яндекс Карты - альтернативный способ', {
            'fields': ('yandex_map_embed_code',),
            'classes': ('collapse',),
            'description': 'Если не указаны координаты, можно вставить embed-код из Конструктора Яндекс.Карт'
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_coordinates(self, obj):
        return obj.has_coordinates()
    has_coordinates.boolean = True
    has_coordinates.short_description = 'Координаты'

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)
