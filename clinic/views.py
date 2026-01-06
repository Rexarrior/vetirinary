from django.shortcuts import render
from news.models import News
from contacts.models import ContactInfo
from reviews.models import Review


from core.models import HeroSection, StatItem
from about.models import FeatureItem, AboutPageText


def home(request):
    """Главная страница клиники"""
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:3]
    contact_info = ContactInfo.objects.first()
    reviews = Review.objects.filter(is_published=True)[:3]
    
    hero_section = HeroSection.objects.first()
    stats = StatItem.objects.all()
    features = FeatureItem.objects.all()
    about_text = AboutPageText.objects.first()
    
    return render(request, 'home.html', {
        'latest_news': latest_news,
        'contact_info': contact_info,
        'reviews': reviews,
        'hero_section': hero_section,
        'stats': stats,
        'features': features,
        'about_text': about_text,
    })