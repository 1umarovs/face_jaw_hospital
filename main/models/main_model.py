from django.db import models
from urllib.parse import urlparse, parse_qs

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    class Ordering:
        fields = ['name']
        order_with_respect_to = 'name'
    
class Patients(models.Model):
    video_link = models.URLField()

    def __str__(self):
        return self.video_link
    

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    class Ordering:
        fields = ['video_link']
        order_with_respect_to = 'video_link'