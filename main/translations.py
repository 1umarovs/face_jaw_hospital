from modeltranslation.translator import register, TranslationOptions
from .models import   Operations , Category



@register(Operations)
class OperationsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'date', 'patient')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
