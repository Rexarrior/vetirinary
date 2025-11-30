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
