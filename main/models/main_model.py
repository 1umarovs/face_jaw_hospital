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


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class Ordering:
        fields = ['name']
        order_with_respect_to = 'name'



class Operations(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Operation'
        verbose_name_plural = 'Operations'

    class Ordering:
        fields = ['name']
        order_with_respect_to = 'name'


class OperationsImages(models.Model):
    operation = models.ForeignKey(Operations, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='operation_images/')

    def __str__(self):
        return f"Image for {self.operation.name}"

    class Meta:
        verbose_name = 'Operation Image'
        verbose_name_plural = 'Operation Images'
