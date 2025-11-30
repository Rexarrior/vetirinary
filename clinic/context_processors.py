from contacts.models import ContactInfo


def contact_info(request):
    """Добавляет информацию о контактах во все шаблоны"""
    return {
        'contact_info': ContactInfo.objects.first()
    }

