from django.db import models


class AboutContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "About Content"
    
    def __str__(self):
        return self.title


class Veterinarian(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='vets/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Order of appearance")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Veterinarians"
        ordering = ['order']
    
    def __str__(self):
        return self.name
