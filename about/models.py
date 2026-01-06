from django.db import models


class AboutContent(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Контент страницы 'О нас'"
        verbose_name_plural = "Контент страницы 'О нас'"
    
    def __str__(self):
        return self.title


class Veterinarian(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    position = models.CharField(max_length=100, verbose_name="Должность")
    bio = models.TextField(verbose_name="Биография")
    photo = models.ImageField(upload_to='vets/', blank=True, null=True, verbose_name="Фото")
    order = models.IntegerField(default=0, help_text="Порядок отображения", verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Ветеринар"
        verbose_name_plural = "Ветеринары"
        ordering = ['order']
    
    def __str__(self):
        return self.name


class FeatureItem(models.Model):
    """Элементы секции 'Почему выбирают нас?'"""
    icon = models.CharField(max_length=50, help_text="CSS класс иконки Bootstrap (например: bi-people)", verbose_name="Иконка")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"
        ordering = ['order']

    def __str__(self):
        return self.title


class AboutPageText(models.Model):
    """Текстовые блоки для страницы 'О клинике'"""
    header_title = models.CharField(max_length=200, default="Почему выбирают нас?", verbose_name="Заголовок секции преимуществ")
    header_subtitle = models.TextField(default="Мы создали клинику, в которую хотели бы обратиться сами. Здесь каждый питомец получает внимание и заботу.", verbose_name="Подзаголовок секции преимуществ")
    
    class Meta:
        verbose_name = "Тексты страницы 'О клинике'"
        verbose_name_plural = "Тексты страницы 'О клинике'"

    def __str__(self):
        return "Тексты страницы 'О клинике'"
