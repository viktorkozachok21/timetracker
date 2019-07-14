from django.contrib import admin
from django.urls import path

from django.conf.urls import include
from filebrowser.sites import site
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Tracker.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/filebrowser/', site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
