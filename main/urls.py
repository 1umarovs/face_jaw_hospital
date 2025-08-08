from django.urls import path
from .views import homePage

app_name = 'main'

urlpatterns = [
    path('', homePage.as_view(), name='home'),
]