from django.contrib import admin
from .models import ContactUs , Patients , Operations , OperationsImages , Category
# Register your models here.

admin.site.register(ContactUs)
admin.site.register(Patients)
admin.site.register(Operations)
admin.site.register(OperationsImages)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    