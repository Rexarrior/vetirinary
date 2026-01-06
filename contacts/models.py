from django.db import models


class ContactInfo(models.Model):
    clinic_name = models.CharField(max_length=100, verbose_name="Название клиники")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    working_hours = models.CharField(max_length=200, verbose_name="Часы работы")
    
    # Координаты для Яндекс Карт
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name="Широта",
        help_text="Например: 47.578300"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name="Долгота",
        help_text="Например: 41.099300"
    )
    map_zoom = models.IntegerField(
        default=16,
        verbose_name="Масштаб карты",
        help_text="Значение от 1 до 19 (16-17 для улицы)"
    )
    
    # Оставляем для обратной совместимости
    yandex_map_embed_code = models.TextField(
        blank=True, 
        verbose_name="Embed-код карты",
        help_text="Альтернативный способ: вставьте HTML-код карты из Яндекс.Конструктора"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"
    
    def __str__(self):
        return self.clinic_name
    
    def has_coordinates(self):
        """Проверяет, заданы ли координаты"""
        return self.latitude is not None and self.longitude is not None


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Contact Submissions"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
class ContactsPageText(models.Model):
    """Текстовые блоки для страницы 'Контакты'"""
    header_title = models.CharField(max_length=200, default="Как нас найти", verbose_name="Заголовок страницы")
    header_subtitle = models.TextField(default="Мы всегда на связи и готовы помочь вашим питомцам", verbose_name="Подзаголовок страницы")
    form_title = models.CharField(max_length=200, default="Напишите нам", verbose_name="Заголовок формы")
    
    class Meta:
        verbose_name = "Тексты страницы 'Контакты'"
        verbose_name_plural = "Тексты страницы 'Контакты'"

    def __str__(self):
        return "Тексты страницы 'Контакты'"
