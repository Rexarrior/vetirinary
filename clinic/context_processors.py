from contacts.models import ContactInfo
from core.models import CommonPhrase, SiteSettings


def contact_info(request):
    """Добавляет информацию о контактах во все шаблоны"""
    return {"contact_info": ContactInfo.objects.first()}


def site_content(request):
    """Добавляет настройки сайта и общие фразы во все шаблоны"""
    settings = SiteSettings.objects.first()
    phrases = {p.key: p.text for p in CommonPhrase.objects.all()}

    return {
        "site_settings": settings,
        "common_phrases": phrases,
    }
