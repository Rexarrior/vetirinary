from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from .models import ContactInfo, ContactSubmission
from .forms import ContactForm


def contacts(request):
    contact_info = ContactInfo.objects.first()
    return render(request, 'contacts/contacts.html', {'contact_info': contact_info})


def contact_us(request):
    contact_info = ContactInfo.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact submission
            form.save()
            
            # Send email notification (in a real app, you would configure email settings)
            # For now, we'll just add a success message
            messages.success(request, 'Thank you for your message. We will contact you soon.')
            
            # Redirect to prevent form resubmission
            return render(request, 'contacts/contact_success.html')
    else:
        form = ContactForm()
    
    return render(request, 'contacts/contact_form.html', {
        'form': form,
        'contact_info': contact_info
    })
