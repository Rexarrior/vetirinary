from django.db import models


class ServiceCategory(models.Model):
    """Категория услуг (например: Терапия, Хирургия, Диагностика)"""
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    icon = models.CharField(max_length=50, blank=True, help_text="CSS класс иконки")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Service(models.Model):
    """Конкретная услуга с ценой"""
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name="Категория"
    )
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена (руб.)"
    )
    price_note = models.CharField(
        max_length=100,
        blank=True,
        help_text="Примечание к цене (например: 'от', 'за единицу')",
        verbose_name="Примечание к цене"
    )
    duration = models.CharField(
        max_length=50,
        blank=True,
        help_text="Примерная длительность",
        verbose_name="Длительность"
    )
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.name} - {self.price} руб."
class ServicesPageText(models.Model):
    """Текстовые блоки для страницы 'Услуги и цены'"""
    header_title = models.CharField(max_length=200, default="Наши услуги", verbose_name="Заголовок страницы")
    header_subtitle = models.TextField(default="Полный спектр ветеринарных услуг для здоровья и благополучия ваших питомцев", verbose_name="Подзаголовок страницы")
    
    class Meta:
        verbose_name = "Тексты страницы 'Услуги'"
        verbose_name_plural = "Тексты страницы 'Услуги'"

    def __str__(self):
        return "Тексты страницы 'Услуги'"
