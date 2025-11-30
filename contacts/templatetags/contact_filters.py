from django import template

register = template.Library()


@register.filter
def phone_url(phone):
    """Преобразует телефон в формат для tel: ссылки (убирает пробелы, скобки, дефисы)"""
    if not phone:
        return ''
    return phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')

