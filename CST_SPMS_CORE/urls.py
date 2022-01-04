from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from CST_SPMS_CORE import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CST_SPMS.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
