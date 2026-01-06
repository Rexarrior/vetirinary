from django.shortcuts import render, get_object_or_404
from .models import ServiceCategory, Service, ServicesPageText


def services_list(request):
    """Страница со всеми услугами по категориям"""
    categories = ServiceCategory.objects.filter(is_active=True).prefetch_related(
        'services'
    )
    services_text = ServicesPageText.objects.first()
    
    return render(request, 'services/list.html', {
        'categories': categories,
        'services_text': services_text,
    })


def service_category(request, slug):
    """Услуги в конкретной категории"""
    category = get_object_or_404(ServiceCategory, slug=slug, is_active=True)
    services = category.services.filter(is_active=True)
    services_text = ServicesPageText.objects.first()
    
    return render(request, 'services/category.html', {
        'category': category,
        'services': services,
        'services_text': services_text,
    })


def prices(request):
    """Прайс-лист - все услуги с ценами"""
    categories = ServiceCategory.objects.filter(is_active=True).prefetch_related(
        'services'
    )
    services_text = ServicesPageText.objects.first()
    
    return render(request, 'services/prices.html', {
        'categories': categories,
        'services_text': services_text,
    })
