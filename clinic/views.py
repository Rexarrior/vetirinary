from django.shortcuts import render
from news.models import News
from contacts.models import ContactInfo


def home(request):
    # Get latest 3 news articles
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:3]
    contact_info = ContactInfo.objects.first()
    
    return render(request, 'home.html', {
        'latest_news': latest_news,
        'contact_info': contact_info
    })