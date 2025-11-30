from django.shortcuts import render
from .models import Review


def reviews_list(request):
    """Страница с отзывами клиентов"""
    reviews = Review.objects.filter(is_published=True)
    return render(request, 'reviews/list.html', {
        'reviews': reviews
    })
