from django.db import models


class Review(models.Model):
    """Отзыв клиента"""
    RATING_CHOICES = [
        (5, '★★★★★'),
        (4, '★★★★☆'),
        (3, '★★★☆☆'),
        (2, '★★☆☆☆'),
        (1, '★☆☆☆☆'),
    ]

    author_name = models.CharField(max_length=100, verbose_name="Имя автора")
    pet_name = models.CharField(max_length=100, blank=True, verbose_name="Имя питомца")
    pet_type = models.CharField(max_length=50, blank=True, verbose_name="Вид питомца")
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст отзыва")
    photo = models.ImageField(
        upload_to='reviews/',
        blank=True,
        null=True,
        verbose_name="Фото"
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author_name} - {self.rating}★"
class ReviewsPageText(models.Model):
    """Текстовые блоки для страницы 'Отзывы'"""
    header_title = models.CharField(max_length=200, default="Отзывы наших клиентов", verbose_name="Заголовок страницы")
    header_subtitle = models.TextField(default="Мы ценим доверие каждого владельца и любовь каждого питомца", verbose_name="Подзаголовок страницы")
    
    class Meta:
        verbose_name = "Тексты страницы 'Отзывы'"
        verbose_name_plural = "Тексты страницы 'Отзывы'"

    def __str__(self):
        return "Тексты страницы 'Отзывы'"
