from django.conf.urls.i18n import set_language
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # 🔹 bu qo‘shilishi kerak
]

urlpatterns += i18n_patterns(
    path('master/', admin.site.urls),
    path('', include('main.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
