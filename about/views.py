from django.shortcuts import render
from .models import AboutContent, Veterinarian, AboutPageText, FeatureItem


def about(request):
    about_content = AboutContent.objects.filter(is_active=True).first()
    veterinarians = Veterinarian.objects.filter(is_active=True).order_by('order')
    about_text = AboutPageText.objects.first()
    features = FeatureItem.objects.all()
    
    return render(request, 'about/about.html', {
        'about_content': about_content,
        'veterinarians': veterinarians,
        'about_text': about_text,
        'features': features,
    })
