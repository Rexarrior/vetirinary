from django.shortcuts import render
from .models import Review, ReviewsPageText


def reviews_list(request):
    """Страница с отзывами клиентов"""
    reviews = Review.objects.filter(is_published=True)
    reviews_text = ReviewsPageText.objects.first()
    
    return render(request, 'reviews/list.html', {
        'reviews': reviews,
        'reviews_text': reviews_text,
    })
