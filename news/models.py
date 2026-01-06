from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title


class NewsPageText(models.Model):
    """Текстовые блоки для страницы 'Новости'"""
    header_title = models.CharField(max_length=200, default="Новости клиники", verbose_name="Заголовок страницы")
    header_subtitle = models.TextField(default="Актуальная информация о жизни клиники и полезные советы для владельцев", verbose_name="Подзаголовок страницы")
    
    class Meta:
        verbose_name = "Тексты страницы 'Новости'"
        verbose_name_plural = "Тексты страницы 'Новости'"

    def __str__(self):
        return "Тексты страницы 'Новости'"
