from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('tasks/', include('tasks.urls')),
    path('', include('users.urls')),
    path('para/', include('para.urls')),
    path('notes/', include('notes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # работа со статикой в режиме разработки (вне-nginx)

if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)