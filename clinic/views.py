from django.shortcuts import render
from news.models import News
from contacts.models import ContactInfo
from reviews.models import Review


def home(request):
    """Главная страница клиники"""
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:3]
    contact_info = ContactInfo.objects.first()
    reviews = Review.objects.filter(is_published=True)[:3]
    
    return render(request, 'home.html', {
        'latest_news': latest_news,
        'contact_info': contact_info,
        'reviews': reviews,
    })