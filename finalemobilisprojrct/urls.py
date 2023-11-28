from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from socialmedia.views import custom_media_serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('socialmedia.urls')),
    path('chat/', include('chatgpt.urls')),
    path('videochat/', include('videocall.urls')),
    path('entertainment/', include('entertainment.urls')),
    path('library/', include('library.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += [path('media/<path:path>/', custom_media_serve)]

# Serving media files during development
# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)