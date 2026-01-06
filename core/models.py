from django.db import models

class SiteSettings(models.Model):
    site_title = models.CharField(max_length=100, default="ВетКлиника", verbose_name="Заголовок сайта")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")
    footer_text = models.TextField(blank=True, verbose_name="Текст в подвале")
    copyright_text = models.CharField(max_length=200, default="© 2025 ВетКлиника. Все права защищены.", verbose_name="Текст копирайта")

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

class CommonPhrase(models.Model):
    key = models.SlugField(unique=True, verbose_name="Ключ (slug)")
    text = models.CharField(max_length=255, verbose_name="Текст")
    description = models.CharField(max_length=255, blank=True, verbose_name="Описание (где используется)")

    class Meta:
        verbose_name = "Общая фраза"
        verbose_name_plural = "Общие фразы"

    def __str__(self):
        return f"{self.key}: {self.text}"

class HeroSection(models.Model):
    badge_location = models.CharField(max_length=100, default="Ветеринарная клиника в Константиновске", verbose_name="Бейдж: Локация")
    badge_work_hours = models.CharField(max_length=100, default="Работаем 24/7", verbose_name="Бейдж: Часы работы")
    badge_license = models.CharField(max_length=100, default="Лицензия", verbose_name="Бейдж: Лицензия")
    title = models.CharField(max_length=255, default="Забота о здоровье ваших питомцев — наша миссия", verbose_name="Заголовок")
    lead_text = models.TextField(default="Современная ветеринарная клиника с опытными специалистами и передовым оборудованием. Мы лечим с любовью!", verbose_name="Лид-текст")
    button_primary_text = models.CharField(max_length=100, default="Записаться на приём", verbose_name="Текст основной кнопки")
    button_secondary_text = models.CharField(max_length=100, default="Наши услуги", verbose_name="Текст вторичной кнопки")

    class Meta:
        verbose_name = "Герой-секция (Главная)"
        verbose_name_plural = "Герой-секция (Главная)"

    def __str__(self):
        return "Контент герой-секции"

class StatItem(models.Model):
    number = models.CharField(max_length=20, verbose_name="Число (например: 15+)")
    label = models.CharField(max_length=100, verbose_name="Подпись")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"
        ordering = ['order']

    def __str__(self):
        return f"{self.number} {self.label}"
