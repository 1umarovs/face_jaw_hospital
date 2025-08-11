from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', homePage.as_view(), name='home'),
    path('category/<slug:slug>/', categoryDetail, name='category_detail'),
]

