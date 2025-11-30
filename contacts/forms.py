from django import forms
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Как к вам обращаться?'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.ru'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Запись на приём / Консультация / Вопрос'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите вашу проблему или вопрос...',
                'rows': 5
            }),
        }
        labels = {
            'name': 'Ваше имя',
            'email': 'Email',
            'phone': 'Телефон',
            'subject': 'Тема обращения',
            'message': 'Сообщение',
        }