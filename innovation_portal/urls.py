from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView  
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('i18n/', include('django.conf.urls.i18n')),
    path('',include('users.urls')),
    path('', include('innovations.urls')),
    path('', include('forum.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)