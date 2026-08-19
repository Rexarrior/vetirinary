"""Bounded read-only data sources for the veterinary clinic assistant."""

from ddgs import DDGS


def get_clinic_info() -> str:
    """
    Получить информацию о ветеринарной клинике: адрес, телефон, email, часы работы.
    Используйте этот инструмент, когда пользователь спрашивает о контактах, 
    местоположении или графике работы клиники.
    """
    from contacts.models import ContactInfo
    
    try:
        contact = ContactInfo.objects.first()
        if contact:
            return f"""
Информация о клинике:
- Название: {contact.clinic_name}
- Адрес: {contact.address}
- Телефон: {contact.phone}
- Email: {contact.email}
- Часы работы: {contact.working_hours}
"""
        return "Контактная информация временно недоступна. Пожалуйста, попробуйте позже."
    except Exception:
        return "Не удалось получить контактную информацию."


def get_services_list() -> str:
    """
    Получить список услуг и цен ветеринарной клиники.
    Используйте этот инструмент, когда пользователь спрашивает об услугах, 
    процедурах или ценах клиники.
    """
    from services.models import ServiceCategory, Service
    
    try:
        categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
        
        if not categories.exists():
            return "Список услуг временно недоступен."
        
        result = "Услуги и цены нашей клиники:\n\n"
        
        for category in categories:
            services = category.services.filter(is_active=True)[:5]  # Limit to 5 per category
            if services:
                result += f"📋 {category.name}:\n"
                for service in services:
                    price_str = f"{service.price} руб."
                    if service.price_note:
                        price_str = f"{service.price_note} {price_str}"
                    result += f"  • {service.name} — {price_str}\n"
                result += "\n"
        
        result += "Для полного списка услуг посетите раздел 'Услуги и цены' на нашем сайте."
        return result
    except Exception:
        return "Не удалось получить список услуг."


def get_veterinarians() -> str:
    """
    Получить информацию о ветеринарах клиники.
    Используйте этот инструмент, когда пользователь спрашивает о врачах, 
    специалистах или команде клиники.
    """
    from about.models import Veterinarian
    
    try:
        vets = Veterinarian.objects.filter(is_active=True)
        
        if not vets.exists():
            return "Информация о врачах временно недоступна."
        
        result = "Наши специалисты:\n\n"
        
        for vet in vets:
            result += f"👨‍⚕️ {vet.name}\n"
            result += f"   Должность: {vet.position}\n"
            if vet.bio:
                # Truncate bio to 150 chars
                bio = vet.bio[:150] + "..." if len(vet.bio) > 150 else vet.bio
                result += f"   {bio}\n"
            result += "\n"
        
        return result
    except Exception:
        return "Не удалось получить информацию о врачах."


def search_veterinary_info(query: str) -> str:
    """
    Поиск информации по ветеринарным темам в интернете.
    Используйте этот инструмент ТОЛЬКО для вопросов о здоровье животных, 
    ветеринарии, уходе за питомцами.
    НЕ используйте для тем, не связанных с животными.
    
    Args:
        query: Поисковый запрос на ветеринарную тему
    """
    # List of veterinary-related keywords to validate query
    vet_keywords = [
        'собака', 'кошка', 'питомец', 'животн', 'ветеринар', 'лечен', 'болезн',
        'симптом', 'вакцин', 'прививк', 'корм', 'уход', 'порода', 'щенок', 'котёнок',
        'котенок', 'хомяк', 'попугай', 'кролик', 'грызун', 'рептили', 'рыбк',
        'аквариум', 'птиц', 'лошад', 'здоровь', 'dog', 'cat', 'pet', 'vet',
        'хвост', 'лап', 'шерст', 'клещ', 'блох', 'глист', 'паразит', 'стерилиз',
        'кастрац', 'операц', 'травм', 'перелом', 'рана', 'инфекц', 'вирус',
        'понос', 'рвот', 'аппетит', 'температур', 'кашел', 'чихан'
    ]
    
    query_lower = query.lower()
    is_vet_related = any(keyword in query_lower for keyword in vet_keywords)
    
    if not is_vet_related:
        return """Извините, я могу искать информацию только по ветеринарным темам. 
Пожалуйста, задайте вопрос о здоровье животных, уходе за питомцами или ветеринарии."""
    
    try:
        # Add veterinary context to the query
        search_query = f"{query} ветеринария"
        
        with DDGS() as ddgs:
            results = list(ddgs.text(search_query, max_results=3))
        
        if not results:
            return """К сожалению, поиск сейчас недоступен. 

Рекомендую:
• Для вопросов о нашей клинике — спросите меня напрямую (я знаю адрес, услуги, цены)
• Для общей информации — посетите проверенные ветеринарные сайты"""
        
        response = "🔍 Результаты поиска:\n\n"
        response += "⚠️ ВАЖНО: Информация из интернета носит ознакомительный характер. "
        response += "Для точного диагноза и лечения обратитесь к ветеринару!\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'Без названия')
            body = result.get('body', '')
            link = result.get('href', '')
            
            # Truncate body
            if len(body) > 200:
                body = body[:200] + "..."
            
            response += f"{i}. **{title}**\n"
            response += f"   {body}\n"
            if link:
                response += f"   Источник: {link}\n"
            response += "\n"
        
        response += "---\n"
        response += "Помните: при любых тревожных симптомах у вашего питомца лучше обратиться к ветеринару лично!"
        
        return response
        
    except Exception as e:
        error_msg = str(e).lower()
        # Handle CAPTCHA and rate limiting
        if 'captcha' in error_msg or 'ratelimit' in error_msg or '202' in error_msg or '403' in error_msg:
            return """Поиск временно недоступен из-за ограничений поисковой системы.

Я могу помочь вам другими способами:
• Расскажу о нашей клинике, услугах и ценах
• Дам общие рекомендации по уходу за питомцами
• Подскажу, когда стоит записаться на приём к ветеринару"""
        
        return """Не удалось выполнить поиск. 

Но я могу помочь:
• Ответить на вопросы о клинике и услугах
• Дать общие советы по уходу за питомцами"""
