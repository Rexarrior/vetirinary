from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactInfo, ContactSubmission, ContactsPageText
from .forms import ContactForm


def contacts(request):
    """Страница контактов с информацией о клинике"""
    contact_info = ContactInfo.objects.first()
    contacts_text = ContactsPageText.objects.first()
    
    return render(request, 'contacts/contacts.html', {
        'contact_info': contact_info,
        'contacts_text': contacts_text,
    })


def contact_us(request):
    """Форма обратной связи / записи на приём"""
    contact_info = ContactInfo.objects.first()
    contacts_text = ContactsPageText.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за обращение! Мы свяжемся с вами в ближайшее время.')
            return redirect('contacts:contact_success')
    else:
        form = ContactForm()
    
    return render(request, 'contacts/contact_form.html', {
        'form': form,
        'contact_info': contact_info,
        'contacts_text': contacts_text,
    })


def contact_success(request):
    """Страница успешной отправки заявки"""
    return render(request, 'contacts/contact_success.html')
