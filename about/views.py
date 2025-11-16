from django.shortcuts import render
from .models import AboutContent, Veterinarian


def about(request):
    about_content = AboutContent.objects.filter(is_active=True).first()
    veterinarians = Veterinarian.objects.filter(is_active=True).order_by('order')
    return render(request, 'about/about.html', {
        'about_content': about_content,
        'veterinarians': veterinarians
    })
